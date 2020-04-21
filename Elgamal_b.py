import socket
import HMAC
import Elgamal
from random import randint as rint

# FILE NOT USEFUL, MADE FOR TESTING

port = 5000


q = Elgamal.q
alpha = Elgamal.alpha
public_key_A = []
random_int = rint(1, q)

message_to_sent = '-__-, HEY, HELLO'

print("I AM SENDING THIS MESSAGE :", message_to_sent)

s = socket.socket()
s.bind(('', port))
s.listen() 
c, addr = s.accept()     
message = c.recv(1024)
message = message.decode()
public_key_A = list(map(int, message.split(" ")))

K = pow(public_key_A[2], random_int, q)
encrypted_message = Elgamal.encrypt(q, alpha, random_int, K, message_to_sent)
print(encrypted_message)
c.send(str.encode(encrypted_message))
s.close()
