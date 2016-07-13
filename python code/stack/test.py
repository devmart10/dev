# testing the stack and the queue

from stack import *
from queue import *

s = Stack()
q = Queue()

test = 'devon martin'

for x in test:
	s.push(x)
	q.enque(x)

print('Popping stack...')
for x in test:
	print(s.pop(), sep='', end='')
print()

print('Dequeing queue...')
for x in test:
	print(q.deque(), sep='', end='')
print()