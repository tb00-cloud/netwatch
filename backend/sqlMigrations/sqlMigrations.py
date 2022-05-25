def __execute(filePath, mysqlobj,  logger):
  """
  Private function to execute SQL staements in a file separated by semi-colon.\n
  Pass a MySQL object, filepath and logger.
  """
  with open(filePath) as file:
    sql = file.read()

    for query in sql.split(';'):
      _, err = mysqlobj.execute(query)
      if err != None:
        logger.critical(err)
        exit(1)

def migrate(mysqlobj, logger):
  """
  Perform a series of SQL script migrations.\n
  Pass a MySQL object and logger.
  """
  migMap = {
    "./backend/sqlMigrations/01.sql"
  }
  
  logger.info("running migrations...")
  for m in migMap:
    logger.debug("running migration %s", m)
    __execute(m, mysqlobj, logger)