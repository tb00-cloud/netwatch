from flask import make_response
from datetime import datetime, timedelta
import base64

#Local import
from backend.http.helpers import httpError, httpSuccess, checkSess
import backend.crypto.crypto as crypto

def getLogin(mysqlobj,request, logger):
  """
  On identification of valid login, returns status 200. Else, returns 204
  """
  sess = request.cookies.get('auth')
  if sess is None:
    return httpSuccess(204)
  else:
    err, valid = checkSess(mysqlobj, sess)
    if err is not None:
      logger.error(err)
      return httpError(500)
    elif valid == True:
      return httpSuccess(200)
    else:
      return httpSuccess(204)

def postLogin(mysqlobj, request, logger):
  """
  Accept valid username and base64-encoded password to return an
  auth cookie (http only, csrf protected) and login state cookie.
  """
  data = request.get_json()

  user = data["username"]
  pwd = base64.b64decode(data["password"]).decode("ascii")
  
  salt, _ = mysqlobj.execute("""SELECT salt FROM users WHERE username = %s AND enabled = 1;""", user)
  
  if len(salt) !=1:
    return httpError(401, body="Invalid username or password")
  spwd = crypto.encrypt(pwd, salt[0][0])
  
  user, _ = mysqlobj.execute("""SELECT ID FROM users WHERE username = %s AND password = %s AND enabled = 1;""", user, spwd)
  if len(user) !=1:
    return httpError(401, body="Invalid username or password")
  else:
    # User exists... generate session
    userId = user[0][0]
    started = datetime.now(tz=None)
    sessID = crypto.randomString(255)
    
    
    exp = datetime.now(tz=None) + timedelta(hours=24)
            
    _, err = mysqlobj.execute("""INSERT INTO userSessions (userID, started, ID, expires) VALUES (%s, %s, %s, %s)""",userId, started, sessID, exp.strftime('%Y-%m-%d %H:%M:%S'))
    
    if err != None:
      logger.error(err)
      return httpError(500)
    
    response = make_response(httpSuccess(200))
    response.set_cookie("auth", sessID, expires=exp, httponly = True, samesite = "Lax")
    response.set_cookie("loginState", "1", expires=exp, samesite = "Lax")
    return response