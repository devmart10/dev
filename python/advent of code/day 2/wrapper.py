with open('input.txt', 'r') as f:

	total = 0

	for line in f.readlines():
		line = line.strip()
		dims = [int(x) for x in line.split('x')]
		areas = [dims[0]*dims[1], dims[1]*dims[2], dims[0]*dims[2]]
		for a in areas:
			total += 2*a
		total += min(areas)
	
	print(total)