class Node:
	def __init__(self, value):
		self.value = value
		self.next = None

# very weird linked list
# can you figure it out..?
class LinkedListStack:
	def __init__(self):
		self.head = None

	def push(self, value):
		# print('val:', value)
		if not self.head:
			# print('Making head')
			self.head = Node(value)
		else:
			i = self.head
			# print('i =', i.value)
			while i.next:
				# print('i has next')
				i = i.next
				# print('i =', i.value)
			# print('i does not have next')
			i.next = Node(value)
			# print('i.next = ', i.next.value)

	def pop(self):
		# print('-'*10)
		if not self.head:
			# print('no head, return none')
			return None
		else:
			# print('has head')
			i = self.head
			self.head = i.next
			return i

LL = LinkedListStack()


s = 'Hello this is a test'

for i, l in enumerate(s):
	print(i, l)
	LL.push(l)


x = LL.pop()
while x:
	print(x.value)
	x = LL.pop()

