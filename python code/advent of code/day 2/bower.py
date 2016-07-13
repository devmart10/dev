with open('input.txt', 'r') as f:

	total = 0

	for line in f.readlines():
		line = line.strip()
		dims = [int(x) for x in line.split('x')]
		dims.sort()
		total += 2*dims[0] + 2*dims[1]
		total += dims[0]*dims[1]*dims[2]
	
	print(total)