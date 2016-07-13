# make "words" the dictionary
words = open('dictionary.txt', encoding='utf8').readlines()
words = [x.strip() for x in words]
#print(words)

# check a document
file = open('file.txt', encoding='utf8').readlines(100)
file = [x.strip() for x in file]
file = [f.split() for f in file]
file_by_words = []
#'''
for line in file:
	for w in line:
		for l in w:
			if not l.isalpha():
				w = w.replace(l, '')
		file_by_words.append(w.lower())


count = 0
for w in file_by_words:
	c = words.count(w)
	if c == 0:
		print(c, '"', w, '"', 'is not in dictionary')
		count += 1
#'''

print('Total misspellings:', count)