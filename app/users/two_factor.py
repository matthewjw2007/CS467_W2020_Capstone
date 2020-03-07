import base64
from time import time
from hashlib import sha1
import hmac
import secrets
import string

def get_totp(secret):
    # Convert secret
    key = base64.b32decode(secret)
    # Get time interval
    message = int(time() // 30).to_bytes(8, byteorder='big')
    # Generate HMAC-SHA1 of message and key
    hash = hmac.new(key=key, msg=message, digestmod=sha1)
    # Truncate the results to get 32-bit number
    strOutput = hash.digest()
    hexOutput = hash.hexdigest()
    offset = int(hexOutput[len(hexOutput) - 1], 16) * 2
    hexSub = hexOutput[offset:(offset+8)]
    truncVal = int(hexSub, 16)
    truncVal = truncVal & 0x7fffffff
    code = truncVal % 1000000
    code = str(code)
    if len(code) < 6:
        while len(code) < 6:
            code = '0' + code
    return code

def generate_secret():
    alphabet = string.ascii_letters + string.digits
    new_string = str()
    for i in range(40):
        new_string = new_string + secrets.choice(alphabet)
    new_string = new_string.encode()
    b32_string = base64.b32encode(new_string)
    secret = b32_string.decode()
    return secret