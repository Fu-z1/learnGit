import os
import binascii

# Returns a random sessiontoken in hex
def getSessiontoken(args, **kwargs):
    return binascii.hexlify(os.urandom(int(args[0]))).decode('utf-8')

manifest = {
    'apiVersion' : "0.2",
    'stringFunctions' : {
        "getSessiontoken" : getSessiontoken
    }
}
