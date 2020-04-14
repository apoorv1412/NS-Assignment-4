import hmac 
import hashlib 

def returnHMAC(key, message):
	return (hmac.new(key.encode(), message.encode(), hashlib.sha256)).hexdigest()