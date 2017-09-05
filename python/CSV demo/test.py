import csv

'''
height
throws
deathYear
bbrefID
nameGiven
deathMonth
nameFirst
weight
birthCity
birthDay
birthCountry
nameLast
deathDay
birthMonth
debut
bats
birthState
deathState
birthYear
finalGame
deathCity
retroID
playerID
deathCountry
'''


def main():
    reader = csv.DictReader(open('data.csv', 'rU'))

    names = {}

    for line in reader:
        if not line['nameFirst'] in names:
        	names[line['nameFirst']] = 0
        else:
        	names[line['nameFirst']] += 1

    for i, name in enumerate(sorted(names.keys(), key=lambda x: names[x])):
    	print(i, name, names[name])

if __name__ == '__main__':
    main()
