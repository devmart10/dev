import textwrap
from nltk.corpus import wordnet as wn

POS = {
    'v': 'verb', 'a': 'adjective', 's': 'satellite adjective',
    'n': 'noun', 'r': 'adverb'}


def get_synonyms(word, pos=None):
    for i, syn in enumerate(wn.synsets(word, pos)):
        syns = [n.replace('_', ' ') for n in syn.lemma_names]
        ants = [a for m in syn.lemmas for a in m.antonyms()]
        ind = ' ' * 12
        meaning = textwrap.wrap(syn.definition, 64)
        print('sense %d (%s)' % (i + 1, POS[syn.pos]))
        print('definition: ' + ('\n' + ind).join(meaning))
        print('  synonyms:', ', '.join(syns))
        if ants:
            print('  antonyms:', ', '.join(a.name for a in ants))
        if syn.examples:
            print('  examples: ' + ('\n' + ind).join(syn.examples))
        print()


def syllables(word):
    count = 0
    vowels = 'aeiouy'
    word = word.lower().strip(".:;?!")
    if word[0] in vowels:
        count += 1
    for index in range(1, len(word)):
        if word[index] in vowels and word[index - 1] not in vowels:
            count += 1
    if word.endswith('e'):
        count -= 1
    if word.endswith('le'):
        count += 1
    if count == 0:
        count += 1
    return count


def main():
    s = 'Here is, a test lyric'
    test_data = s.split()
    c = 0
    for word in test_data:
        c += syllables(word)
        # print(get_synonyms(word))
    print(c)

if __name__ == '__main__':
    main()
