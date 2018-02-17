from collections import defaultdict

text = """
super book
super cat good super
cat good book
"""

print('Variant 1')
pairs = defaultdict(int)
for line in text.split('\n'):
    if line:
        words = line.split()
        for o, i in enumerate(words):
            i = i.lower()
            for j in words[o+1:]:
                j = j.lower()
                pair = (j, i) if i > j else (i, j)
                pairs[pair] += 1

for pair, cnt in pairs.items():
    print('{}|{} - {}'.format(pair[0], pair[1], cnt))

print()

print('Variant 2')
# this book this cat good this cat good book
text = text.replace('\n', ' ')
pairs = defaultdict(int)
words = text.split()
for o, i in enumerate(words):
    i = i.lower()
    for j in words[o+1:]:
        j = j.lower()
        pair = (j, i) if i > j else (i, j)
        pairs[pair] += 1

for pair, cnt in pairs.items():
    print('{}|{} - {}'.format(pair[0], pair[1], cnt))

print()

print('Variant 3')
# mapper
words_cache = []
for line in text.split('\n'):
    if line:
        words = line.split()
        for word in words:
            words_cache.append(word)

# reducer
pairs = defaultdict(int)
for o, i in enumerate(words_cache):
    i = i.lower()
    for j in words_cache[o+1:]:
        j = j.lower()
        pair = (j, i) if i > j else (i, j)
        pairs[pair] += 1

for pair, cnt in pairs.items():
    print('{}|{} - {}'.format(pair[0], pair[1], cnt))
