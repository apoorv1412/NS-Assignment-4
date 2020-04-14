import socket
import HMAC

port = 5000
key = 'secret key'

s = socket.socket()  
s.bind(('', port))
s.listen()         
c, addr = s.accept()     
message = c.recv(1024)
message = message.decode()
s.close()

plaintext, received_mac = message.split('||')
print ('plaintext = ', plaintext)
print ('received_mac = ', received_mac)
computed_mac = HMAC.returnHMAC(key = key, message = plaintext)
print ('computed_mac = ', computed_mac)
if computed_mac == received_mac:
	print ('message has been authenticated')
else:
	print ('something is wrong')