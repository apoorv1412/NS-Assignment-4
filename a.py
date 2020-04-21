import socket
import HMAC
import RSA
import datetime
import Elgamal
from random import randint as rint

port_1 = 10012
port_2 = 2012
port = 5012

q = Elgamal.q
alpha = Elgamal.alpha

secret_key_A_HMAC = 'secret key_A '
secret_key_AB_HMAC = ''

private_key_A = 100015691
public_key_KDA = 199570405
public_key_B = -1

def format(msg):
	return msg.split('||')

'''
Sending request to KDA asking for public key of B
'''       
s = socket.socket() 
s.connect(('127.0.0.1', port_1))
time_now = datetime.datetime.now()
message = 'Connection request of B' + '||' + str(time_now)
s.send(str.encode(message))
reply = s.recv(1024)
reply = reply.decode()
decrypted_reply = RSA.decrypt(reply, RSA.n, public_key_KDA)
decrypted_reply = format(decrypted_reply)

public_key_B = int(decrypted_reply[0])
time_from_reply = datetime.datetime.strptime(decrypted_reply[2], '%Y-%m-%d %H:%M:%S.%f')

if(abs((time_now - time_from_reply).total_seconds()) > 1):
	print("message time out")

if(decrypted_reply[1] != format(message)[0]):
	print("Message Corrupt")

print ('Got public key of B', public_key_B) 
s.close()




# Deriving the secret key for HMAC Algorithm

s = socket.socket()  
s.bind(('', port))
s.listen()         
c, addr = s.accept()     
message = c.recv(1024)
message = message.decode()

decrypted_message = RSA.decrypt(message, RSA.n, private_key_A)
secret_key_AB_HMAC = secret_key_A_HMAC + decrypted_message
print("HMAC key derived-:", secret_key_AB_HMAC)

reply = secret_key_A_HMAC
encrypted_reply = RSA.encrypt(reply, RSA.n, public_key_B)
c.send(str.encode(encrypted_reply))



# Secret key for hmac derived for both A,B


# Now the transfer of three messages Hello1, Hello2, Hello3 begins
for _ in range(3):
	# New key everytime
	XA = rint(1, q - 1)
	YA = pow(alpha, XA, q)

	public_key_A = [q, alpha, YA]
	private_key_A = YA

	plaintext = str(q) + " " + str(alpha) + " " + str(YA)

	message = plaintext + '||' + HMAC.returnHMAC(key = secret_key_AB_HMAC, message = plaintext)

	c.send(str.encode(message))

	reply = c.recv(2048).decode()

	C1, C2, recv_mac = reply.split("||")

	computed_mac = HMAC.returnHMAC(key = secret_key_AB_HMAC, message = C1 + "||" + C2)

	if(computed_mac != recv_mac):
		print("MAC ERROR")

	decrypted_message = Elgamal.decrypt(q, XA, C1 + "||" + C2)

	print("I have received this message -",decrypted_message)




c.close()
s.close()
