from flask import Flask, request, make_response
from waitress import serve
from flask_httpauth import HTTPBasicAuth
from functools import wraps
from flask_cors import CORS

#Local import
from backend.http.helpers import httpError, checkSess
from backend.http.users import getUsers, putUsers, deleteUsers
from backend.http.targets import getTargets, putTargets, deleteTargets
from backend.http.login import getLogin, postLogin
from backend.http.logout import postLogout
from backend.logger import logger

app = Flask(__name__) 
cors = CORS(app, supports_credentials=True)
auth = HTTPBasicAuth()

# WRAPPERS
#######################

def debugLogger(f):
  """
  Produces standard route debug logs
  """
  @wraps(f)
  def wrapper(*args, **kwargs):
    app.logger.debug("serving request. url:%s method:%s", request.url, request.method)
    return f(*args, **kwargs)
  return wrapper

def requireJsonType(f):
  """
  Check content-type is application/json when there is request data
  """
  @wraps(f)
  def wrapper(*args, **kwargs):
    if request.content_type != 'application/json' and (request.data):
      return httpError(400, body='Content type must be application-json')
    return f(*args, **kwargs)
  return wrapper

# Authenticated endpoints
def loginRequired(f):
  """
  Authenticated endpoints
  """
  @wraps(f)
  def wrapper(*args, **kwargs):
    sess = request.cookies.get('auth')
    if sess is None:
      return httpError(401, body="Unuathorized")
    else:
      err, valid = checkSess(app.config["MYSQLOB"], sess)
      
      if err is not None:
        logger.error(err)
        return httpError(500)
      
      if valid == False:
        response = make_response(httpError(401, body="Unuathorized"))
        response.delete_cookie('auth')
        response.delete_cookie('loginState')
        return response
      else:
        return f(*args, **kwargs)
  return wrapper

# HTTP ROUTES
#######################

@app.route('/targets', methods=['GET', 'PUT', 'DELETE'])
@requireJsonType
# @loginRequired
@debugLogger
def targets():
  if request.method == 'GET':
    return getTargets(app.config["MYSQLOB"], request, app.logger)
  elif request.method == 'PUT':
    return putTargets(app.config["MYSQLOB"], request, app.logger)
  elif request.method == 'DELETE':
    return deleteTargets(app.config["MYSQLOB"], request, app.logger)

@app.route('/users', methods=['GET', 'DELETE', 'PUT'])
@loginRequired
@requireJsonType
@debugLogger
def users():
  if request.method == 'GET':
    return getUsers(app.config["MYSQLOB"], request, app.logger)
  elif request.method == 'PUT':
    return putUsers(app.config["MYSQLOB"], request, app.logger)
  elif request.method == 'DELETE':
    return deleteUsers(app.config["MYSQLOB"], request, app.logger)


@app.route('/login', methods=['POST', 'GET'])
@requireJsonType
@debugLogger
def login():
  if request.method=='GET':
    return getLogin(app.config["MYSQLOB"], request, app.logger)
  if request.method=='POST':
    return postLogin(app.config["MYSQLOB"], request, app.logger)

@app.route('/logout', methods=['POST'])
@debugLogger
def logout():
  return postLogout(app.config["MYSQLOB"], request, app.logger)

# HTTP APP ENTRYPOINT
#######################
def run(mysqlobj, logger):
  
  
  logger.info("starting HTTP application...")
  app.config["MYSQLOB"] = mysqlobj
  # app.config["LOGGER"] = logger
    
  key, err = mysqlobj.execute('SELECT value FROM sysConfig WHERE name = "flaskSessionKey";')
  
  if err is not None:
    logger.error(err)
    return err
  
  if len(key) != 1:
    return 'Unexpected number of results returned when retrieving Flask session key' 
  
  app.config['SECRET_KEY'] = key[0][0]
  app.logger = logger
  app.logger.propagate = False
  # app.run(port=5000)
  serve(app, host="0.0.0.0", port=5000)
