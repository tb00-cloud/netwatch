import mysql
import mysql.connector
from time import sleep

class connectionDtls: 
  """
  MySQL class to set up MySQL connection. Arguments: \n
  host      - MySQL server address \n
  port      - MySQL server listening port \n
  user      - login username \n 
  password  - login password \n
  db        - name of DB to run queries against
  """
  def __init__(self, host, user, password, port, db): 
    self.host = host 
    self.user = user
    self.password = password
    self.port = port
    self.db = db

class MySQL: 
  """
  MySQL class with methods to abstract logic to execute SQL statements with retry: \n
  cnxDtls       - connectiond etails. See connectionDtls class \n
  retryAttempts - upon connection error, number of attempts to try before failure \n
  retryDelay    - upon connection error, how long to wait before retrying \n 
  logger        - logger
  """
  connection = None
  session = None

  def __init__(self, cnxDtls, retryAttempts, retryDelay, logger): 
    self.host = cnxDtls.host 
    self.user = cnxDtls.user
    self.password = cnxDtls.password
    self.port = cnxDtls.port
    self.db = cnxDtls.db
    self.retryAttempts = retryAttempts
    self.retryDelay = retryDelay
    self.logger = logger
  
  def open(self):
    maxAttempts = self.retryAttempts
    delay = self.retryDelay

    attempts = 1

    while attempts <= maxAttempts:
      try:
        self.connection = mysql.connector.connect(
          host=self.host,
          database=self.db,
          user=self.user,
          password=self.password,
          port=self.port,
          autocommit=True
        )
      except mysql.connector.Error as e:
        self.logger.error("error while connecting to MySQL. Trying again... error:[%d]: %s" % (e.args[0], e.args[1]))
        attempts += 1
        sleep(delay)
      else:
        break
        
    if self.connection is None:
      return ("could not open connection with MySQL server.")
    
    while attempts <= maxAttempts:
      try:
        self.session = self.connection.cursor()
      except mysql.connector.Error as e:
        self.logger.critical("error while opening MySQL session cursor. Trying again... error:[%d]: %s" % (e.args[0], e.args[1]))
        attempts += 1
        sleep(delay)
      else:
        break
    
    if self.session is None:
        return ("could not open session cursor with MySQL server. Application will exit")
  
  def close(self):
    self.connection.close()
    self.session.close()

  def execute(self,statement, *args):
    err = self.open()
    if err != None:
      return None, err
    try:
      self.session.execute(statement, args)
    except mysql.connector.Error as e:
      err = "MySQL error [%d]: %s" % (e.args[0], e.args[1])
      self.close()
      return None, err
    else:
      records = []
      if self.session.description is None:
        # No recordset for INSERT, UPDATE, CREATE. Return empty
        self.close()
        return records, None
      else:
        # Fetch records and return
        records = self.session.fetchall()
        self.close()
        return records, None
