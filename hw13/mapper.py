#!/usr/bin/env python3

import re
import sys

# Список стоп-слов прямо из NLTK
STOP_WORDS = {
    'i',
    'me',
    'my',
    'myself',
    'we',
    'our',
    'ours',
    'ourselves',
    'you',
    'your',
    'yours',
    'yourself',
    'yourselves',
    'he',
    'him',
    'his',
    'himself',
    'she',
    'her',
    'hers',
    'herself',
    'it',
    'its',
    'itself',
    'they',
    'them',
    'their',
    'theirs',
    'themselves',
    'what',
    'which',
    'who',
    'whom',
    'this',
    'that',
    'these',
    'those',
    'am',
    'is',
    'are',
    'was',
    'were',
    'be',
    'been',
    'being',
    'have',
    'has',
    'had',
    'having',
    'do',
    'does',
    'did',
    'doing',
    'a',
    'an',
    'the',
    'and',
    'but',
    'if',
    'or',
    'because',
    'as',
    'until',
    'while',
    'of',
    'at',
    'by',
    'for',
    'with',
    'about',
    'against',
    'between',
    'into',
    'through',
    'during',
    'before',
    'after',
    'above',
    'below',
    'to',
    'from',
    'up',
    'down',
    'in',
    'out',
    'on',
    'off',
    'over',
    'under',
    'again',
    'further',
    'then',
    'once',
    'here',
    'there',
    'when',
    'where',
    'why',
    'how',
    'all',
    'any',
    'both',
    'each',
    'few',
    'more',
    'most',
    'other',
    'some',
    'such',
    'no',
    'nor',
    'not',
    'only',
    'own',
    'same',
    'so',
    'than',
    'too',
    'very',
    's',
    't',
    'can',
    'will',
    'just',
    'don',
    'should',
    'now',
}

# Удалим все знаки препинания, оставим только символы ', -, ., ?, !
delete_punctuation = re.compile(r'[^a-zA-Z0-9\-\s\'.?!]\s*')
# Удалим все отдельно стоящие цифры
delete_numbers = re.compile(r'\b[\d]+\b')
# Удалим все односимвольные объекты
delete_single = re.compile(r'(?:^|\s)[\w\'\-](?:\s|$)(?:[\w\'\-](?:\s|$))*')
# Уберем все лишнее с конца и начала строки
delete_tails = re.compile(r'(?:\b|^)[\'\-]+\B|\B[\'\-]+(?:\b|$)')
# Уберем все отступы которые могли образоваться перед .?!
delete_extra_spaces = re.compile(r'\s+([.?!])+')
# Если слово является концом предложения
sentence_sentinel = re.compile(r'[\-\']*[.?!]+[\-\']*$')
# Уберем все лишние знаки препинания с конца строки
delete_sentence_sentinels = re.compile(r'[\-\']*[.?!]+[\-\']*')


def build_sentence(buffer, sentence, line=None):
    if line:
        buffer.extend(line.lower().split())
    for o, word in enumerate(buffer):
        if sentence_sentinel.search(word):
            word = delete_sentence_sentinels.sub('', word)
            sentence.append(word)
            return buffer[o+1:], sentence
        sentence.append(word)
    return [], sentence


def sentence_to_pairs(sentence):
    cache = set()
    for o, i in enumerate(sentence):
        for j in sentence[o+1:]:
            if i == j or {i, j} & STOP_WORDS:
                continue
            pair = (j, i) if i > j else (i, j)
            if pair in cache:
                continue
            cache.add(pair)
            print('{}|{}\t1'.format(pair[0], pair[1]))


def main():
    buffer = []
    sentence = []
    for line in sys.stdin:
        line = line.strip('\n')
        if line:
            line = delete_punctuation.sub(' ', line)
            line = delete_numbers.sub(' ', line)
            line = delete_single.sub(' ', line)
            line = delete_tails.sub('', line)
            line = delete_extra_spaces.sub('\1', line)
            buffer, sentence = build_sentence(buffer, sentence, line)
            if buffer:
                sentence_to_pairs(sentence)
                sentence = []
    _, sentence = build_sentence(buffer, sentence)
    sentence_to_pairs(sentence)


main()
