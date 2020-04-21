

q = 761
alpha = 6


def encrypt(q, alhpa, random_int, K, message_to_sent):
	C1 = ""
	C2 = ""

	for c in message_to_sent:
		C1 += str(pow(alhpa, random_int, q)) + " "
		C2 += str((K * ord(c)) % q) + " "

	C1 = C1[:len(C1) - 1]
	C2 = C2[:len(C2) - 1]

	return C1 + "||" + C2


def decrypt(q, XA, encrypted_message):
	C1, C2 = encrypted_message.split("||")
	decrypted_message = ""

	C1 = list(map(int, C1.split(" ")))
	C2 = list(map(int, C2.split(" ")))

	if len(C1) != len(C2):
		print("SOMETHING WRONG")

	for i in range(len(C1)):
		K = pow(C1[i], XA, q)
		M = (C2[i] * pow(K, q - 2, q)) % q
		decrypted_message += chr(M)

	return decrypted_message