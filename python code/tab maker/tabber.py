'''
Program for creating a tabluture template
Creates a file "tab.txt"

PARAMETERS
lines: number of lines

measures: measures per line

subdiv: dashes per measure
'''

# CONSTANTS
strings = 'eBGDAE'

# safe open
with open('tab.txt', 'w') as f:
	# number of lines
	lines = 4
	
	# measures per line
	measures = 4
	
	# dashes per measure
	subdiv = 16	

	# go through number of lines
	for l in range(lines):

		# do each line by doing each guitar string sequencially
		for s in strings:
		
			# print string number to start each line
			f.write(s)

			# for number of measures per string
			for m in range(measures):
				f.write('|')
				f.write('-' * subdiv)

			# newline for next string
			f.write('|\n')

		# newline between lines
		f.write('\n')