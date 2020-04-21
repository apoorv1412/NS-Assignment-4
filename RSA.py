
block_size = 30
p = 45293
q = 45389
phi = (p-1)*(q-1)
n = 2055803977

def encrypt(message, n, e):
	binary_string = ''
	for a in message:
		b = bin(ord(a))[2:]
		b = '0'*(8-len(b)) + b
		binary_string += b
	rem = len(binary_string) % block_size
	binary_string += '1'
	binary_string += (block_size-rem-1)*'0'

	encrypted_string = ''

	num_blocks = len(binary_string) // block_size
	for i in range(num_blocks):
		curr = binary_string[i * block_size : (i + 1) * block_size]
		curr = int(curr,2)
		curr = pow(curr,e,n)
		encrypted_string += str(curr)
		encrypted_string += ' '
	return encrypted_string

def decrypt(message, n, d):
	binary_string = ''
	message = message.rstrip(' ')
	message = list(map(int, message.split()))
	for a in message:
		curr = a
		curr = pow(curr,d,n)
		curr = bin(curr)[2:]
		curr = '0' * (block_size - len(curr)) + curr
		binary_string += curr

	y = binary_string

	binary_string = binary_string.rstrip('0')
	binary_string = binary_string[:len(binary_string) - 1]
	
	decrypted_string = ''
	num_chars = len(binary_string) // 8

	for i in range(num_chars):
		curr = binary_string[i * 8 : (i + 1) * 8]
		curr = int(curr,2)
		decrypted_string += chr(curr)

	return decrypted_string



