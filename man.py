import nltk


def function(item):
    entries = nltk.corpus.cmudict.entries()
    return entries[BinarySearch(entries, item)][1]


def BinarySearch(lys, val):
    first = 0
    last = len(lys)-1
    index = -1
    while (first <= last) and (index == -1):
        mid = (first+last) // 2
        if lys[mid][0] == val:
            index = mid
        else:
            if val < lys[mid][0]:
                last = mid - 1
            else:
                first = mid + 1
    return index

print(function("door"))
print(function("floor"))