def checkBadStrings(s):
	badwords = ['ab', 'cd', 'pq', 'xy']
	good = True
	for word in badwords:
		if word in s:
			good = False
			break
	return good

def checkVowels(s):
	vowels = 'aeiou'
	count = 0
	for letter in s:
		if letter in vowels:
			count += 1
	return count >= 3

def checkDouble(s):
	double = False
	for i, l in enumerate(s[:-1]):
		if s[i] == s[i + 1]:
			double = True
			break
	return double

def checkPairs(s):
	pair = False
	for i, l in enumerate(s[:-2]):
		group = s[i:i + 2]
		if group in s[i+2:]:
			pair = True
			break
	return pair

def checkRepeat(s):
	repeat = False
	for i, l in enumerate(s[:-2]):
		if s[i] == s[i + 2]:
			repeat = True
			break
	return repeat

def runChecks(s):
	return checkPairs(s) and checkRepeat(s)

# testing
# s = 'ieodomkazucvgmuy'
# print(runChecks(s))

# '''
with open('input.txt', 'r') as f:
	lines = f.readlines()
	count = 0
	for i, line in enumerate(lines):
		if runChecks(line.strip()):
			count += 1

	print(count)

# '''