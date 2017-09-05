with open('input.txt', 'r') as f:
	line = f.readline()

	total = 1
	pos = [0, 0]
	visited = []
	visited.append((pos[0], pos[1]))

	for x in line:
		# print(pos)
		if x == '^':
			pos[1] += 1
		if x == 'v':
			pos[1] -= 1
		if x == '<':
			pos[0] -= 1
		if x == '>':
			pos[0] += 1

		if (pos[0], pos[1]) not in visited:
			# print(pos)
			visited.append((pos[0], pos[1]))
			total += 1

	print(total)