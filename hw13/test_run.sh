#!/usr/bin/env bash

cat alice.txt | ./mapper.py | sort | ./reducer.py | sort -r -n -k 2 | head -n 200 > tests/test_top_200_pairs.txt
cat alice.txt | ./mapper.py | sort | ./reducer.py | wc -l > tests/test_pairs_count.txt