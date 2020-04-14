import socket
import HMAC

port = 5000
key = 'secret key'

s = socket.socket()  
s.connect(('127.0.0.1', port))
plaintext = 'This is a message to test hmac'
message = plaintext + '||' + HMAC.returnHMAC(key = key, message = plaintext)
s.send(str.encode(message))
s.close()
