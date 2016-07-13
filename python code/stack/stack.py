# implementing a stack in Python

class Stack:
	def __init__(self):
		self.array = []

	def isEmpty(self):
		return self.array == []

	def push(self, value):
		self.array.append(value)

	def pop(self):
		return self.array.pop()

	def peek(self):
		return self.array[-1]

	def size(self):
		return len(self.array)