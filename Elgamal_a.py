import socket
import HMAC
import Elgamal
from random import randint as rint

# FILE NOT USEFUL, MADE FOR TESTING

port = 5000

q = Elgamal.q
alpha = Elgamal.alpha

XA = rint(1, q - 1)
YA = pow(alpha, XA, q)

public_key_A = [q, alpha, YA]
private_key_A = YA


s = socket.socket()  
s.connect(('127.0.0.1', port))
plaintext = str(q) + " " + str(alpha) + " " + str(YA)
message = plaintext
s.send(str.encode(message))

encrypted_message = s.recv(1024).decode()
decrypted_message = Elgamal.decrypt(q, XA, encrypted_message)

print("I GOT THIS MESSAGE :", decrypted_message)

s.close()
