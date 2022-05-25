import os
from multiprocessing import Process

# Import local
import backend.sqlMigrations.sqlMigrations as sqlMigrations
import backend.mysqlc.mysqlc as mysqlc
import backend.targetCNX.targetCNX as targCnx
import backend.http.http as http
import backend.crypto.crypto as crypto
import backend.logger.logger as logger
import backend.webSessions.webSessions as webSessions

class config(mysqlc.connectionDtls):
  def __init__(self):
    self.coreLogLevel = os.environ.get('CORE_LOG_LEVEL', 'info').upper()
    self.HTTPLogLevel = os.environ.get('HTTP_LOG_LEVEL', 'debug').upper()
    self.runMigs = os.getenv("RUN_MIGRATIONS", 'true').lower() in ('true', '1', 't')
    
    self.sqlPort = os.environ.get('MYSQL_PORT', 3306)

    self.errors = []
    
    self.sqlHost = os.environ.get('MYSQL_HOST', None)
    if self.sqlHost is None:
      self.errors.append("MYSQL_HOST env var cannot be blank")
    
    self.sqlDB = os.environ.get('MYSQL_DB', None)
    if self.sqlDB is None:
      self.errors.append("MYSQL_DB env var cannot be blank")
    
    self.sqlUser = os.environ.get('MYSQL_USER', None)
    if self.sqlUser is None:
      self.errors.append("MYSQL_USER env var cannot be blank")
        
    self.sqlPassword = os.environ.get('MYSQL_PASSWORD', None)
    if self.sqlPassword is None:
      self.errors.append("MYSQL_PASSWORD env var cannot be blank")
    
    self.rootUser = os.environ.get('ROOT_USER', None)
    
    self.rootPassword = os.environ.get('ROOT_PASSWORD', None)
    if self.rootUser is not None and self.rootPassword is None:
      self.errors.append("ROOT_PASSWORD env var cannot be blank if ROOT_USER is set")

        
    self.sqlPassword = os.environ.get('MYSQL_PASSWORD', None)
    if self.sqlPassword is None:
      self.errors.append("MYSQL_PASSWORD env var cannot be blank")
    
    super().__init__(self.sqlHost, self.sqlUser, self.sqlPassword, self.sqlPort, self.sqlDB)
        
def initRootUser(mysqlobj, cfg, logger):
  if cfg.rootUser is not None:
    logger.debug("checking for root user: %s", cfg.rootUser)
    records, err = mysqlobj.execute("""select username from users where username = %s;""", cfg.rootUser)
    
    if err != None:
      return err
    
    if len(records) > 0:
      logger.debug("root user already exists")
      return None
    else:
      logger.info("no root user exists. Creating...")
      pwdPlain = cfg.rootPassword
      pwdPlain = "root"
      pwd, psalt = crypto.new(pwdPlain)
    
      logger.info('root user created. Username: root Password: %s' % (pwdPlain))
      _, err = mysqlobj.execute("""INSERT INTO users (username, password, salt) VALUES (%s, %s, %s)""" , cfg.rootUser,pwd, psalt)
      
      if err != None:
        return err
  else:
    logger.debug("ROOT_USER env var not set. Skipping root user setup")
    return None
    
if __name__ == "__main__":
  cfg = config()
    
  coreLogger, err = logger.LoggerFactory.get_logger("CORE", logLevel=cfg.coreLogLevel, mode="json")
  if err is not None:
    print(err)
    exit(1)
    
  HTTPLogger, err = logger.LoggerFactory.get_logger("HTTP", logLevel=cfg.HTTPLogLevel, mode="json")
  if err is not None:
    print(err)
    exit(1)

  coreLogger.info("starting application...")

  if len(cfg.errors) > 0:
    for e in cfg.errors:
      coreLogger.critical("application initilisation error: %s" % (e))
    exit(1)

  coreLogger.debug('configuring MySQL connection. host=%s;database=%s;user=%s;port=%s' % (cfg.host, cfg.db, cfg.user, cfg.port))
  coreMysqlobj = mysqlc.MySQL(cfg, 2, 2, coreLogger)
  
  if cfg.runMigs is True:
    sqlMigrations.migrate(coreMysqlobj, coreLogger)
  else:
    coreLogger.info("migrations skipped")
  
  err = initRootUser(coreMysqlobj, cfg, coreLogger)
  if err != None:
    coreLogger.critical(err)
    exit(1)
  
  err = webSessions.initSessionKey(coreMysqlobj, coreLogger)
  if err != None:
    coreLogger.critical(err)
    exit(1)
  
  p = Process(target=webSessions.purgeSessions, args=(coreMysqlobj,coreLogger))
  p.daemon = True
  p.start()
  
  HTTPMysqlobj = mysqlc.MySQL(cfg, 2, 2, HTTPLogger)

  p = Process(target=http.run, args=(HTTPMysqlobj,HTTPLogger))
  p.daemon = True
  p.start()

  targCnx.handler(coreMysqlobj,coreLogger)
 