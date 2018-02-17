#!/usr/bin/env python3

import re
import sys

# Список стоп-слов прямо из NLTK
from collections import defaultdict

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
delete_tails = re.compile(r'(?:\b[\'\-]+\B|\B[\'\-]+\b)')
# Уберем все лишние знаки препинания с конца строки
delete_sentence_sentinels = re.compile(r'[.?!]+$')


def build_sentence(line, buffer, sentence):
    sentence_sentinels = ('.', '!', '?',)
    buffer.extend(line.split())
    for o, word in enumerate(buffer):
        if word.endswith(sentence_sentinels):
            word = delete_sentence_sentinels.sub('', word)
            sentence.append(word.lower())
            return buffer[o+1:], sentence
        sentence.append(word.lower())
    return [], sentence


def sentence_to_pairs(sentence):
    pairs_cache = defaultdict(int)
    for o, i in enumerate(sentence):
        for j in sentence[o+1:]:
            if i == j or {i, j} & STOP_WORDS:
                continue
            pair = (j, i) if i > j else (i, j)
            pairs_cache[pair] += 1

    for pair, cnt in pairs_cache.items():
        print('{}|{}\t{}'.format(pair[0], pair[1], cnt))


def main():
    buffer = []
    sentence = []
    for line in sys.stdin:
        if line:
            line = delete_punctuation.sub(' ', line)
            line = delete_numbers.sub(' ', line)
            line = delete_single.sub(' ', line)
            line = delete_tails.sub('', line)
            buffer, sentence = build_sentence(line, buffer, sentence)
            if buffer:
                sentence_to_pairs(sentence)
                sentence = []
    sentence_to_pairs(sentence)


main()
