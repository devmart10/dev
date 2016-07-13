from stack import *

# user = input('Enter your name to see it reversed: ')
user = 'Devon Martin'
user = user.lower()

s = Stack()
for i in user:
	s.push(i)

print('Your name backwards:')
for i in user:
	print(s.pop(), sep='', end='')
print()