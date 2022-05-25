from flask import make_response

#Local import
from backend.http.helpers import httpError, httpSuccess

def postLogout(mysqlobj, request, logger):
  sess = request.cookies.get('auth')
  if sess is None:
    return httpSuccess(200)
  else:
     _, err = mysqlobj.execute("""DELETE FROM userSessions WHERE ID = %s""", sess)
     
     if err != None:
      logger.error(err)
      return httpError(500)
    
  response = make_response(httpSuccess(200))
  response.delete_cookie('auth')
  response.delete_cookie('loginState')
  return response