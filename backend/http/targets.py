import validators, re
from datetime import datetime, timedelta

#Local import
from backend.http.helpers import httpError, httpSuccess

class target:
  class history:
    def __init__(self,timestamp,status,outcome):
      self.timestamp = timestamp
      self.status = status
      self.outcome = outcome
     
  def __init__(self,ID,name,host,port,enabled,interval,retentionVal,retentionUnit,history):
    self.ID = ID
    self.name = name
    self.host = host
    self.port = port
    self.enabled = enabled
    self.interval = interval
    self.retentionVal = retentionVal
    self.retentionUnit = retentionUnit
    self.history = history

def getTargets(mysqlobj,request,logger):
  tIDs = request.args.get('target_ids')
  wHist = request.args.get('with_history')
  hFrom = request.args.get('history_from') 
  hTo = request.args.get('history_to')
  
  if hFrom is not None:
    if hTo is None:
      return httpError(400, body="if history_from is set, history_to must also be set")    
  
  if hTo is not None:
    if hFrom is None:
      return httpError(400, body="if history_to is set, history_from must also be set")
  
  if hFrom is not None and hTo is not None:
    hFrom = datetime.utcfromtimestamp(int(hFrom)).strftime('%Y-%m-%d %H:%M:%S')
    hTo = datetime.utcfromtimestamp(int(hTo)).strftime('%Y-%m-%d %H:%M:%S')
    
    if hFrom >= hTo:
      return httpError(400, body="history_from must be before history_to", )
  else:
    # history range not set, we will set a default 
    now = datetime.now(tz=None)
    hFrom = (now - timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
    hTo = now.strftime('%Y-%m-%d %H:%M:%S')
  
  
  targets = []
  
  if tIDs is not None:
    idList = tIDs.split(",")
    records = []
    for id in idList:
      rec, err = mysqlobj.execute("""SELECT ID, name, host, port, enabled, inter, retentionVal, retentionUnit FROM targets WHERE ID = %s;""", id)
      if err is not None:
        logger.error(err)
        return httpError(500)
      if len(rec) == 1:
        records.append(rec[0])
  else:
    records, err = mysqlobj.execute("""SELECT ID, name, host, port, enabled, inter, retentionVal, retentionUnit FROM targets;""")
  
  if err is not None:
    logger.error(err)
    return httpError(500)
  else:
    for row in records:
      
      ID = row[0]
      name = row[1]
      host = row[2]
      port = row[3]
      enabled = row[4]
      interval = row[5]
      retentionVal = row[6]
      retentionUnit = row[7]
      
      tHist = []
      
      if wHist is not None and wHist.lower() == "true":
        history, err = mysqlobj.execute("""SELECT a.timestamp, b.name FROM connResults AS a JOIN statusCodes AS b ON a.statusID = b.ID WHERE a.targetID = %s AND a.timestamp >= %s AND a.timestamp <= %s ORDER BY a.timestamp ASC;""", ID, hFrom, hTo)
        
        if err is not None:
          logger.error(err)
          return httpError(500)
        
        for h in history:
          timestamp = h[0]
          status = h[1]
          if status != "success" :
            outcome = 0
          else:
            outcome = 1
                  
          hist = target.history(timestamp.strftime('%Y-%m-%dT%H:%M:%SZ'),status,outcome)
          tHist.append(hist.__dict__)
        
      targ = target(ID, name,host, port, enabled, interval,retentionVal,retentionUnit,tHist)
      targets.append(targ.__dict__)

  return httpSuccess(200,body=targets)

def __putTargetValidation(id,name,host,port,interval,retentionVal,retentionUnit):
  
  errors = []
  
  if not str(id).isdigit() and id is not None:
    errors.append({"id":"must be a number"})
  
  nameRegex = re.compile("^[A-Za-z0-9 _-]*$")  
  if name is None or len(name) > 255 or not nameRegex.match(name):
    errors.append({"name": "must be less than 255 charatcers, contain letters, numbers, spaces, underscores, hiphens"})
  
  if (not validators.domain(host) and not validators.ipv4(host) and not validators.ipv6(host)) or len(host) > 255 or host is None:
    errors.append({"host": "must be valid domain, ipv4, ipv6"})

  if not str(port).isdigit() or len(str(port)) >= 5 or port is None:
    errors.append({"port": "must be a number, less than 6 digits, not null"})

  if not str(interval).isdigit() or len(str(interval)) > 10 or interval is None or int(interval) < 2:
    errors.append({"interval": "must be a number, less than 10 digits, greater than 2, not null"})
  
  if not str(retentionVal).isdigit() or len(str(retentionVal)) > 10 or retentionVal is None:
    errors.append({"retentionVal": "must be a number, less than 10 digits, not null"})
  
  if retentionUnit not in ('MINUTE','HOUR','DAY','WEEK','MONTH','QUARTER','YEAR'):
    errors.append({"retentionUnit": "must be a one of MINUTE, HOUR, WEEK, MONTH, QUARTER, YEAR"})

  if len(errors) >0:
    return False, errors
  return True, None


def putTargets(mysqlobj,request, logger):
  data = request.get_json()
  
  if data:
    if 'id' in data and data['id'] != "":
      id = data['id']
    else:
      id = None
      
  if data:
    if 'name' in data:
      name = data['name']
    else:
      name = None

    if 'host' in data:
      host = data['host']
    else:
      host = None
        
    if 'port' in data:
      port = data['port']
    else:
      port = None
        
    if 'enabled' in data:
      
      enabled = data['enabled']
      if not isinstance(enabled, bool):
        if str(enabled).lower() in ('true','t','1'):
          enabled = True
        if str(enabled).lower() in ('false','f','0'):
          enabled = False
        
    else:
      enabled = False
        
    if 'interval' in data:
      interval = data['interval']
    else:
      interval = 5
        
    if 'retentionVal' in data:
      retentionVal = data['retentionVal']
    else:
      retentionVal = 7
        
    if 'retentionUnit' in data:
      retentionUnit = data['retentionUnit']
    else:
      retentionUnit = 'DAY'
  
  if name is None or host is None or port is None:
    return httpError(400, body="payload is invalid. missing required attribute(s)")
  
  violations, errors = __putTargetValidation(id,name,host,port,interval,retentionVal,retentionUnit)
  if violations is not True:
    return httpError(400, body=errors) 
  
  if id is not None:
    _, err = mysqlobj.execute("""UPDATE targets SET name=%s,host=%s,port=%s,enabled=%s,inter=%s,retentionVal=%s,retentionUnit=%s WHERE ID=%s;""", name,host,port,enabled,interval,retentionVal,retentionUnit,id)
  else:
    _, err = mysqlobj.execute("""INSERT INTO targets (name, host, port, enabled, inter, retentionVal, retentionUnit) VALUES (%s,%s,%s,%s,%s,%s,%s);""",name,host,port,enabled,interval,retentionVal,retentionUnit)

  if err is not None:
    logger.error(err)
    return httpError(500)
  
  return httpSuccess(200)

def deleteTargets(mysqlobj,request, logger):
  tIDs = request.args.get('target_ids')
  if tIDs is None:
    httpError(400, body="target ids parameter cannot be empty")
  
  idList = tIDs.split(",")
  for id in idList:
    _, err = mysqlobj.execute("""DELETE FROM targets WHERE ID = %s;""", id)
    if err is not None:
      logger.error(err)
      return httpError(500)
  
  return httpSuccess(200)