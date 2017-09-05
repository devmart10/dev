strongTo = {
    'normal'    : ['ghost*'],
    'fire'      : ['steel', 'fire', 'grass', 'ice', 'bug', 'fairy'],
    'water'     : ['fire', 'water', 'ice', 'steel'],
    'grass'     : ['water', 'grass', 'electric', 'ground'],
    'electric'  : ['electric', 'flying', 'steel'],
    'flying'    : ['ground*', 'grass', 'fighting', 'bug'],
    'ground'    : ['electric*', 'rock', 'poison'],
    'rock'      : ['poison', 'normal', 'fire', 'flying'],
    'fighting'  : ['dark', 'rock', 'bug'],
    'ice'       : ['ice'],
    'poison'    : ['poison', 'bug', 'fairy', 'fighting', 'grass'],
    'bug'       : ['fighting', 'grass', 'ground'],
    'ghost'     : ['normal*', 'fighting*', 'poison', 'bug'],
    'psychic'   : ['psychic', 'fighting'],
    'dragon'    : ['electric', 'fire', 'water', 'grass'],
    'dark'      : ['psychic*', 'dark', 'ghost'],
    'fairy'     : ['dragon*', 'dark', 'fighting', 'bug'],
    'steel'     : ['ice', 'normal', 'grass', 'flying', 'rock', 'poison*', 'psychic', 'dragon', 'fairy', 'steel', 'bug']
}

weakTo = {
    'normal'    : ['fighting'],
    'fire'      : ['water', 'ground', 'rock'],
    'water'     : ['grass', 'electric'],
    'grass'     : ['fire', 'flying', 'ice', 'poison', 'bug'],
    'electric'  : ['ground'],
    'flying'    : ['electric', 'rock', 'ice'],
    'ground'    : ['water', 'grass', 'ice'],
    'rock'      : ['water', 'grass', 'ground', 'fighting', 'steel'],
    'fighting'  : ['flying', 'psychic', 'fairy'],
    'ice'       : ['fire', 'rock', 'fighting', 'steel'],
    'poison'    : ['ground', 'psychic'],
    'bug'       : ['fire', 'flying', 'rock'],
    'ghost'     : ['ghost', 'dark'],
    'psychic'   : ['bug', 'ghost', 'dark'],
    'dragon'    : ['ice', 'dragon', 'fairy'],
    'dark'      : ['fighting', 'bug', 'fairy'],
    'fairy'     : ['poison', 'steel'],
    'steel'     : ['fire', 'ground', 'fighting']
}

def getWeakness(t):
    if t in weakTo.keys():
        return weakTo[t]
    else:
        return []

def getStrength(t):
    if t in strongTo.keys():
        return strongTo[t]
    else:
        return []

def main():
    t = input('enter type: ')
    while t:
        print('\nWeak to:')
        for x in getWeakness(t):
            print('    -', x)
        print('\n* indicates immunity')
        print('Resistant to:')
        for x in getStrength(t):
            print('    +', x)
        t = input('\nenter type: ')

if __name__=='__main__':
    main()