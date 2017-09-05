from hashlib import md5

def getHex(s, i):
	return md5((s + str(i)).encode()).hexdigest()

s = 'ckczppom'
i = 0
while(getHex(s, i)[:6] != '000000'):
	i += 1

print(i)
