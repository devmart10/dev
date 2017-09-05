# class for light object
class light:
    def __init__(self):
        self.brightness = 0

    def turnOff(self):
        if not self.brightness == 0:
            self.brightness -= 1

    def turnOn(self):
        self.brightness += 1

    def toggle(self):
        self.brightness += 2

# utility func for sanitizing input
# returns command, c1, c2
def sanitize(line):
    line = line.strip()
    line = line.split(' ')

    command = None
    if len(line) == 4:
        command = 'toggle'
        c1 = [int(n) for n in line[1].split(',')]
        c2 = [int(n) for n in line[3].split(',')]
    else:
        c1 = [int(n) for n in line[2].split(',')]
        c2 = [int(n) for n in line[4].split(',')]

        if line[1] == 'on':
            command = 'on'
        else:
            command = 'off'

    return command, c1, c2


# array init
arr = [[light() for x in range(1000)] for y in range(1000)]

# open file
with open('input.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        command, c1, c2 = sanitize(line)
        for row in arr[c1[1]:c2[1] + 1]:
            for col in row[c1[0]:c2[0] + 1]:
                if command == 'toggle':
                    col.toggle()
                elif command == 'on':
                    col.turnOn()
                else:
                    col.turnOff()

    count = 0
    for row in arr:
        for col in row:
            count += col.brightness
    print(count)
# '''
