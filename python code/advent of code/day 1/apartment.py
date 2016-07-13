with open('input.txt', 'r') as f:
	line = f.readline()
	i = 0
	c = 0
	for x in line:
		c += 1
		if(x == '('):
			i += 1
		else:
			i -= 1

		if i < 0:
			break;

	print('char:', c)
