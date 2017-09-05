'''
123 -> x            x = 123
456 -> y            y = 456
x AND y -> d        d = AND(x, y)
x OR y -> e         e = OR(x, y)
x LSHIFT 2 -> f     f = LSHIFT(x, 2)
y RSHIFT 2 -> g     g = RSHIFT(y, 2)
NOT x -> h          h = NOT(x)
NOT y -> i          i = NOT(y)
'''
keywords = ['AND', 'OR', 'LSHIFT', 'RSHIFT', 'NOT']

def sanitize(line):
    line = line.strip()
    line = line.split('->')
    left, right = line[0].strip(), line[1].strip()
    left = left.split(' ')
    things = left + [right]
    command = None
    for x in things:
        if x in keywords:
            command = x
            things.remove(x)

    return command, things

def AND(in1, in2):
    return in1 & in2

def OR(in1, in2):
    return in1 | in2

def LSHIFT(in1, in2):
    return in1 << in2

def RSHIFT(in1, in2):
    return in1 >> in2

def NOT(in1):
    return ~ in1 & 0xFFFF

knownInputs = {}
lines = []
with open('input.txt', 'r') as f:
    lines = f.readlines(45)

# recursive function
def getVal(in1):
    # if found, return it
    if in1 in knownInputs.keys():
        print('*'*5, 'found', in1)
        return knownInputs[in1]

    # find line where in1 first recieves input
    for line in lines:
        command, v = sanitize(line)
        # if recieving inputs
        if v[-1] == in1:
            break

    # check if those inputs have values yet
    for x in v[:-1]:
        v1 = getVal(x)
        v2 = 

    # 
    # TRAIN OF THOUGHT
    # 
    # Trying to recursively

    if not command:
        try:
            knownInputs[v[-1]] = int(v[0])
            return int(v[0])
        except: pass
    else:
        # switch/case on command
        if command == 'NOT':
            return NOT(getVal(v[0]))
        else:
            return 0



    # return (command, v[:-1])



# main control loop
for line in lines:
    command, v = sanitize(line)
    print(v[-1], '=', getVal(v[-1]))

print('\nKnown Values')
for x in knownInputs.keys():
    print(x, knownInputs[x])