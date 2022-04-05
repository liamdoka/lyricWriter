import json
from random import randint
import nltk

def rhymesWith(word1, word2, level):
    return word1[1][-level:] == word2[1][-level:]

## BEGIN ##
with open('data.json', 'r') as infile:
    data = json.load(infile)

data = sorted(data, key=lambda datum: len(datum[0]))

# Check if any of the lines rhyme
lines = []
for x in range(len(data)):
    for y in range(x+1, len(data)):
        if data[x][2][0] == data[y][2][0] or abs(data[x][1] - data[y][1]) >= 2:
            continue
        elif rhymesWith(data[x][2], data[y][2], 2):
            lines.append((data[x][0], data[y][0]))

# Picks some pseudo-random variables
x = randint(0, len(lines)-1)
y = randint(x, len(data))
z = randint(-10,5)
a = lines[x]

# Prints the random verse
print(data[y][0])
print(a[0])
print(data[y+z][0])
print(a[1])