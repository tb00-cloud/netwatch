from datetime import datetime
from time import sleep

#local import
import backend.crypto.crypto as crypto

def initSessionKey(mysqlobj, logger):
  """
  Set up the http session key.
  """
  logger.debug("checking for flask session key")
  records, err = mysqlobj.execute("""select name from sysConfig where name = "flaskSessionKey";""")
  
  if err != None:
    return err
  
  if len(records) > 0:
    logger.debug("flask session key already exists")
    return None
  else:
    logger.info("no flask session key exists. Creating...")
    sessionKey = crypto.randomString(255)
    _, err = mysqlobj.execute('INSERT INTO sysConfig (name, value) VALUES ("flaskSessionKey", "%s")' % (sessionKey))
    if err != None:
      return err
    
def purgeSessions(mysqlobj, logger):
  """
  Infinite loop to purge expired web sessions.
  """
  logger.info("starting web session purge job...")
  while True:
    
    now = datetime.now(tz=None).strftime('%Y-%m-%d %H:%M:%S')
    logger.debug("cleaning up web sessions that expired before: %s" % (now))
      
    _, err = mysqlobj.execute("""DELETE from userSessions where expires < %s""",  now)

    if err is not None:
      logger.error("cannot purge web sessions. MySQL error ocurred: %s" % (err))

    sleep(10)