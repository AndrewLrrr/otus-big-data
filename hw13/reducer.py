#!/usr/bin/env python3

import sys
from itertools import groupby

for key, group in groupby((l.split('\t') for l in sys.stdin), key=lambda x: x[0]):
    print('{}\t{}'.format(key, sum(int(g[1]) for g in group)))
