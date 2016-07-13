with open('input.txt', 'r') as f:
	line = f.readline()

	total = 1
	s_pos = [0, 0]
	r_pos = [0, 0]
	# bool for taking turns
	santa = True

	visited = []
	visited.append((s_pos[0], s_pos[1]))

	for x in line:
		if x == '^':
			if santa:
				s_pos[1] += 1
			else:
				r_pos[1] += 1

		if x == 'v':
			if santa:
				s_pos[1] -= 1
			else:
				r_pos[1] -= 1

		if x == '<':
			if santa:
				s_pos[0] -= 1
			else:
				r_pos[0] -= 1

		if x == '>':
			if santa:
				s_pos[0] += 1
			else:
				r_pos[0] += 1

		if santa and (s_pos[0], s_pos[1]) not in visited:
			visited.append((s_pos[0], s_pos[1]))
			total += 1
		elif (r_pos[0], r_pos[1]) not in visited:
				visited.append((r_pos[0], r_pos[1]))
				total += 1

		santa = not santa

	print(total)