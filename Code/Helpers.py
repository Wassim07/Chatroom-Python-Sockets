import hashlib
from Cryptodome.Cipher import AES
import sys

reload(sys)  # Reload does the trick!
sys.setdefaultencoding('iso-8859-1')


class Helpers(object):
    @staticmethod
    def hash(key):
        
        return hashlib.sha256(str.encode(key)).digest()



    @staticmethod
    def encrypt(secret,data):
        # Because the block size is 16 bytes, the way to handle this is to add padding when encrypting.
        # otherwise we'll receive this error :
        # ValueError: Input strings must be a multiple of 16 in length
        message = str.encode(data)
        while len(message) % 16 != 0:
            message = " " + message

        secret=b'12345678azertyui12345678azertyui'
        return AES.new(str.encode(secret), AES.MODE_ECB).encrypt(message)



    @staticmethod
    def decrypt(secret,data):
        secret=b'12345678azertyui12345678azertyui'
        return AES.new(secret, AES.MODE_ECB).decrypt(data)
