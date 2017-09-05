# implementing a stack in Python

class Queue:
	def __init__(self):
		self.array = []

	def isEmpty(self):
		return self.array == []

	def enque(self, value):
		self.array.append(value)

	def deque(self):
		return self.array.pop(0)

	def peek(self):
		return self.array[-1]

	def size(self):
		return len(self.array)