import socket, random
from time import sleep
from multiprocessing import Process, Queue
from datetime import datetime

class target:
  def __init__(self,ID,name,host,port,enabled,interval,queue):
    self.ID = ID
    self.name = name
    self.host = host
    self.port = port
    self.enabled = enabled
    self.queue = queue
    self.interval = interval
    self.logCtx = 'ID=%s host=%s port=%s enabled=%s interval=%s' % (self.ID, self.host, self.port, self.enabled, self.interval)
    
    if interval > 60:
      self.timeout = 60
    else:
      self.timeout = interval
  
  def __refresh(self,mysqlobj, logger):
    """
    private method to re-feth target config.
    """
    logger.debug("refreshing target info for: %s" % (self.logCtx))
    records, err = getTargets(mysqlobj, logger, self.ID)
     
    if err is not None:
      return err
    
    if len(records) > 0:
      self.host = records[0][1]
      self.port = records[0][2]
      self.enabled = records[0][3]
      self.interval = records[0][4]
      self.logCtx = 'ID=%s host=%s port=%s enabled=%s interval=%s' % (self.ID, self.host, self.port, self.enabled, self.interval)

  def connect(self, queue, mysqlobj, logger):
    """
    method for target to run connection attempts.
    """
    rand = random.randint(1, 10)
    logger.debug("starting connection: %s in %s seconds" % (self.logCtx, rand))
    sleep(rand)
    
    while queue.empty() == True:
      err = self.__refresh(mysqlobj, logger)
      
      if err is not None:
        logger.error("error refreshing info for target. Further checks may not reflect changes made to the target until a further refresh is successful: %s" % (self.logCtx))
      result = 0
      s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      s.settimeout(self.timeout)
      
      try: 
        s.connect((self.host, self.port)) 
      except socket.herror as e:
        result = 1 #generic error
        logger.debug("connection failure generic: %s" % (self.logCtx))
      except socket.gaierror as e:
        result = 2 #name resolution error
        logger.debug("connection failure name resolution: %s" % (self.logCtx))
      except socket.timeout as e:
        result = 3 #timeout error
        logger.debug("connection failure timeout: %s" % (self.logCtx))
      except socket.error as e:
        result = 1 #generic error
        logger.debug("connection failure generic: %s" % (self.logCtx))
      else:
        logger.debug("connection success: %s" % (self.logCtx))
      finally:
        s.close 
      
      conf, err = mysqlobj.execute('SELECT ID FROM targets where ID = %s;' % (self.ID))

      if err != None:
        logger.error("cannot record connection attempt in database for: %s. MySQL error ocurred: %s" % (self.logCtx, err))
        continue
      
      if len(conf) > 0:
        logger.debug("recording connection attempt in database: %s - result: %s" % (self.logCtx, result))
        
        stmt = ('INSERT INTO connResults (timestamp, targetID, statusID) VALUES ("%s",%s,%s);' % (datetime.utcnow(), self.ID, result))
        _, err = mysqlobj.execute(stmt)

        if err != None:
          logger.error("cannot record connection attempt in database for: %s. MySQL error ocurred: %s" % (self.logCtx, err))
          continue
      else:
        logger.debug("skipping recording of connection attempt in database. Target has been deleted: %s" % (self.logCtx))
          
      # End of loop 
      sleep(self.interval)

def getTargets(mysqlobj,logger, id=None):
  """
  Retrieve targets from database.\n
  Pass a MySQL object, logger and optional target ID. 
  """
  logger.debug("getting targets from DB with ID: %s", id)
  
  if id is not None:
    records, err = mysqlobj.execute('select ID, host, port, enabled, inter, retentionVal, retentionUnit from targets where ID = %s;', id)
  else:
    records, err = mysqlobj.execute('select ID, host, port, enabled, inter, retentionVal, retentionUnit from targets;')

  if err != None:
    logger.error("cannot retrieve targets from database. MySQL error ocurred: %s" % (err))
    return None, err
  return records, None


# targetHandler
# Execute the target handler responsible for discovering new targets and executing connection daemons. 
def handler(mysqlobj, logger):
  """
  Package handler. Responsible for handling target daemons.\n
  Pass a MySQL object and logger.
  """
  logger.info("starting target handling job...")
  p = Process(target=purgeHistory, args=(mysqlobj,logger))
  p.daemon = True
  p.start()
  
  targets = {}

  while True:
    dbTargets = {}

    records, err = getTargets(mysqlobj, logger)

    if err != None:
      logger.error("cannot retrieve targets from database. MySQL error ocurred: %s" % (err))
      continue

    for row in records:
      ID = row[0]
      host = row[1]
      port = row[2]
      enabled = row[3]
      interval = row[4]

      logCtx = 'ID=%s host=%s port=%s' % (ID, host, port)
      
      q = Queue()

      if ID in targets:
        if enabled == 0:
          targets[ID].queue.put(1)
          logger.info("cancelling target: %s" % (logCtx))
          targets.pop(ID)
          continue
      else:
        if enabled == 1:
          logger.info("identified new target. Daemon starting for: %s" % (logCtx))

          newTarget = target(ID, None, host, port, enabled, interval, q)
          targets[ID]=newTarget

          p = Process(target=newTarget.connect, args=(q,mysqlobj,logger))
          p.daemon = True
          p.start()
    
      # Collect dictionary of DB targets to compare against in-memory targets. 
      newDBTarget = target(ID, None, host, port, enabled, interval, q)
      dbTargets[ID] = newDBTarget

    
    for ID in list(targets):
      if ID not in dbTargets:
        logger.info("target no longer found in database. Daemon closing for: %s" % (targets[ID].logCtx))
        targets[ID].queue.put(1)
        targets.pop(ID)
        
    # End of loop 
    sleep(5)

def purgeHistory(mysqlobj, logger):
  """
  Separate to the main handler. Responsible for routinely purging target history.\n
  Pass a MySQL object and logger.
  """
  logger.info("starting history purge job...")
  while True:
    
    now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    records, err = getTargets(mysqlobj, logger)
    
    if err != None:
      logger.error("cannot retrieve targets from database. MySQL error ocurred: %s" % (err))
      continue
      
    for row in records:
      ID = row[0]
      host = row[1]
      port = row[2]
      retentionVal = row[5]
      retentionUnit = row[6]

      logCtx = 'ID=%s host=%s port=%s retention=%s%ss' % (ID, host, port, retentionVal, retentionUnit)
      
      logger.debug("cleaning up expired history records for: %s" % (logCtx))
      
      stmt = ('delete from connResults where targetID = %s and DATE_ADD(timestamp, INTERVAL %s %s) < "%s";' % (ID,retentionVal,retentionUnit.upper(),now))
      _, err = mysqlobj.execute(stmt)

      if err != None:
        logger.error("cannot delete connection result data from database. MySQL error ocurred: %s" % (err))
      continue
    
    # End of loop 
    sleep(10)