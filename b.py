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

private_key_B = 100093193
public_key_KDA = 199570405
public_key_A = -1
secret_key_B_HMAC = 'secret key_B'
secret_key_AB_HMAC = ''

def format(msg):
	return msg.split('||')


'''
Sending request to KDA asking for public key of A
'''     

s = socket.socket()          
s.connect(('127.0.0.1', port_2))
time_now = datetime.datetime.now()
message = 'Connection request of A' + '||' + str(time_now)
# Connection request of A
s.send(str.encode(message))

reply = s.recv(1024)
reply = reply.decode()
decrypted_reply = RSA.decrypt(reply, RSA.n, public_key_KDA)
decrypted_reply = format(decrypted_reply)
public_key_A = int(decrypted_reply[0])
time_from_reply = datetime.datetime.strptime(decrypted_reply[2], '%Y-%m-%d %H:%M:%S.%f')

if(abs((time_now - time_from_reply).total_seconds()) > 1):
	print("message time out")
	exit()
if(decrypted_reply[1] != format(message)[0]):
	print("Message Corrupt")
	exit()

print ('Got public key of A', public_key_A)
s.close()





# Deriving the secret key for HMAC Algorithm

s = socket.socket()  
s.connect(('127.0.0.1', port))
plaintext = secret_key_B_HMAC
encrypted_text = RSA.encrypt(plaintext, RSA.n, public_key_A)
s.send(str.encode(encrypted_text))
reply = s.recv(1024)
reply = reply.decode()
decrypted_reply = RSA.decrypt(reply, RSA.n, private_key_B)
secret_key_AB_HMAC = decrypted_reply + secret_key_B_HMAC
print("HMAC key derived-:", secret_key_AB_HMAC)



# Secret key for hmac derived for both A,B


# Now the transfer of three messages Hello1, Hello2, Hello3 begins
msgs = ['Hello1', 'Hello2', 'Hello3']

for _ in range(3):

	print("I am sending -:", msgs[_])
	message = s.recv(2048)
	message = message.decode()
	public_key_A, received_mac = message.split("||")

	computed_mac = HMAC.returnHMAC(key = secret_key_AB_HMAC, message = public_key_A)

	if(computed_mac != received_mac):
		print("MAC ERROR")

	q, alpha, YA = list(map(int, public_key_A.split(" ")))

	random_int = rint(1, q)

	K = pow(YA, random_int, q)
	encrypted_message = Elgamal.encrypt(q, alpha, random_int, K, msgs[_])

	message_to_be_sent = encrypted_message + "||" + HMAC.returnHMAC(key = secret_key_AB_HMAC, message = encrypted_message)

	s.send(str.encode(message_to_be_sent))



s.close()
