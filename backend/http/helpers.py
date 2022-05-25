from flask import jsonify
from datetime import datetime

class __error:
  def __init__(self, msg):
    self.error = msg

def httpError(code, body="internal server error"):
  err = __error(body)
  return jsonify(err.__dict__), code

def httpSuccess(code, body=None):
  if body is None:
    body = {}
  try:
    return jsonify(body), code
  except Exception:
    return httpError(500)

# Check if session exists in databases and is valid
# Returns error and bool
def checkSess(mysqlobj, sess):
  now = datetime.now(tz=None).strftime('%Y-%m-%d %H:%M:%S')
  valid, err = mysqlobj.execute("""SELECT ID from userSessions where ID = %s AND expires > %s""", sess, now)
  
  if err is not None:
    return err, None

  if len(valid)!=1:
    return None, False
  
  return None, True