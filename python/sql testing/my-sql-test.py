import sqlite3
conn = sqlite3.connect('example.db')
C = conn.cursor()

C.execute('''
	CREATE TABLE person
	(id INTEGER PRIMARY KEY ASC, name varchar(250) NOT NULL)
		''')

C.execute('''
	CREATE TABLE address
	(id INTEGER PRIMARY KEY ASC, street_name varchar(250), street_number varchar(250), post_code varchar(250) NOT NULL, person_id INTEGER NOT NULL, FOREIGN KEY(person_id) REFERENCES person(id))
		''')

C.execute('''
	INSERT INTO person VALUES (1, 'Devon Martin')
		''')

C.execute('''
	INSERT INTO address VALUES (1, 'Maureen Ln', '390', '94523', 1)
		''')

conn.commit
conn.close