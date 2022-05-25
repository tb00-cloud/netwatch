import os
import hashlib
import secrets, string
from base64 import b64encode

def new(plaintext):
  salt = b64encode(os.urandom(64)).decode("ascii")
  return encrypt(plaintext, salt), salt

def encrypt(plaintext, salt):
  return hashlib.pbkdf2_hmac('sha256', plaintext.encode(), salt.encode(), 10000).hex()

def safeAlphabet():
  return string.ascii_letters + string.digits + "~=-_()£$%&!-.?@#|"

def randomString(length):
  alphabet = safeAlphabet()
  str = ''.join(secrets.choice(alphabet) for i in range(length)) 
  return str
