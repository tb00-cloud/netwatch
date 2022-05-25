import backend.crypto.crypto as crypto
import base64, re

#Local import
from backend.http.helpers import httpError, httpSuccess

class user:
  def __init__(self,ID,username,enabled):
    self.ID = ID
    self.username = username
    self.enabled = enabled

def getUsers(mysqlobj, request, logger):
  uIDs = request.args.get('user_ids')
   
  users = []
  
  if uIDs is not None:
    idList = uIDs.split(",")
    records = []
    for id in idList:
      rec, err = mysqlobj.execute("""SELECT ID, username, enabled FROM users WHERE ID = %s;""", id)
      if err is not None:
        logger.error(err)
        return httpError(500)
      if len(rec) == 1:
        records.append(rec[0])
  else:
    records, err = mysqlobj.execute("""SELECT ID, username, enabled FROM users;""")
  
  if err is not None:
    logger.error(err)
    return httpError(500)
  else:
    for row in records:
      
      ID = row[0]
      username = row[1]
      enabled = row[2]  
        
      usr = user(ID, username, enabled,)
      users.append(usr.__dict__)

  return httpSuccess(200, body=users)


def deleteUsers(mysqlobj,request, logger):
  uIDs = request.args.get('user_ids')
  if uIDs is None:
    httpError(400, body="user ids parameter cannot be empty")
  
  idList = uIDs.split(",")
  for id in idList:
    _, err = mysqlobj.execute("""DELETE FROM users WHERE ID = %s;""", id)
    if err is not None:
      logger.error(err)
      return httpError(500)
  
  return httpSuccess(200)

def __putUserValidation(id,username,password=False):
  
  if not str(id).isdigit() and id is not None:
    return False
  
  usernameRegex = re.compile("^[A-Za-z0-9 _-]*$")  
  if username is None or len(username) > 255 or not usernameRegex.match(username):
    return False
  
  if password != False: #a default value of false for password allows function consumers to not validate passwords. 
    if password is None or len(password) > 255:
      return False
    
    regex = re.compile("^(?=.*[0-9])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{6,128}$")
    if not regex.match(password):
      return False

  return True

def putUsers(mysqlobj,request, logger):
  data = request.get_json()
  
  if data:
    if 'id' in data and data['id'] != "":
      id = data['id']
    else:
      id = None
      
  if data:
    if 'username' in data:
      username = data['username']
    else:
      username = None

    if 'password' in data:
      password = base64.b64decode(data['password']).decode("ascii")
    else:
      password = None
      
    if 'new_password' in data:
      newPassword = base64.b64decode(data['new_password']).decode("ascii")
    else:
      newPassword = None
        
    if 'enabled' in data:
      
      enabled = data['enabled']
      if not isinstance(enabled, bool):
        if str(enabled).lower() in ('true','t','1'):
          enabled = True
        if str(enabled).lower() in ('false','f','0'):
          enabled = False
    else:
      enabled = False
  
  if id is not None: # updating user 
    if newPassword is not None: # with new password
      violations = __putUserValidation(id,username, newPassword)
      if violations is not True:
        return httpError(400, body="Invalid request")
                       
      pwdPlain = newPassword
      pwd, salt = crypto.new(pwdPlain)
      _, err = mysqlobj.execute("""UPDATE users SET username=%s,salt=%s,password=%s,enabled=%s WHERE ID=%s;""", username,salt, pwd,enabled,id)
    else: #updating user but not with new password
      violations = __putUserValidation(id,username)
      if violations is not True:
        return httpError(400, body="Invalid request") 
      _, err = mysqlobj.execute("""UPDATE users SET username=%s,enabled=%s WHERE ID=%s;""", username,enabled,id)
      
    if err is not None:
      logger.error(err)
      return httpError(500)
    
  else: # Not updating a user, putting one
    violations = __putUserValidation(id,username,password)
    if violations is not True:
      return httpError(400, body="Invalid request")  
    
    dupe, err = mysqlobj.execute("""SELECT id FROM users WHERE username=%s;""", username)
    
    pwdPlain = password
    pwd, salt = crypto.new(pwdPlain)  
      
    if err is not None:
      logger.error(err)
      return httpError(500)

    if len(dupe) > 0:
      return httpError(400, body="this username is already taken")
  
    _, err = mysqlobj.execute("""INSERT INTO users (username, salt, password, enabled) VALUES (%s,%s,%s,%s);""",username,salt, pwd,enabled)

  if err is not None:
    logger.error(err)
    return httpError(500)
  
  return httpSuccess(200)