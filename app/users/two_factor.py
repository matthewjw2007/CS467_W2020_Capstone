import base64
from time import time
from hashlib import sha1
import hmac

def getTOTP(secret):
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