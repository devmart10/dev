import json
import yaml

# helper functions
from funcs import *

# for money formatting
from re import sub
from decimal import Decimal


with open('data.json') as data_file:
	# needed so data wasn't unicode
	data = yaml.safe_load(data_file)

streetDB = {}
total = 0
for ticket in data:
	# these are strings
	id = ticket['id']
	date = ticket['date']

	address = ticket['streetAddress']
	street = get_street(address)
	add_street(street, streetDB)

	cost = ticket['cost']
	total += Decimal(sub(r'[^\d.]', '', cost))


print '$' + str(total)

copy = streetDB.copy()
for street in copy:
	if copy[street] == 0:
		del streetDB[street]

# sort that shit
for s in sorted(streetDB, key=streetDB.get, reverse=True):
	print s, ':', streetDB[s]