def get_street(address):
	temp = address.split(' ')
	return temp[1] + ' ' + temp[2]

def add_street(street, database):
	if database.has_key(street):
		database[street] += 1
	else:
		database[street] = 0