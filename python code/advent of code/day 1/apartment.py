with open('input.txt', 'r') as f:
	line = f.readline()
	i = 0
	for x in line:
		if(x == '('):
			i += 1
		else:
			i -= 1

	print(i)