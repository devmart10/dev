import csv

def main():
	reader = csv.reader(open('data.csv', 'rU'))

	words = {}

	for line in reader:
		for word in line:
			if not words.has_key(word):
				words[word] = 0
			else:
				words[word] += 1

	copy = words.copy()
	for word in words:
		if words[word] == 0:
			#print str(word) + ': ' + str(words[word])
			del copy[word]

	words = copy

	for word in sorted(words, key=words.get, reverse=True):
  		print word, words[word]

  	print '\nNumber of Unique Entries:', len(words)

if __name__ == '__main__':
	main()