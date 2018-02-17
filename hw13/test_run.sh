#!/usr/bin/env bash

cat alice_texts/alice_1.txt alice_texts/alice_2.txt alice_texts/alice_3.txt | ./mapper.py | sort | ./reducer.py | sort -r -n -k 2 | head -n 200 > tests/test_top_200_pairs.txt
cat alice_texts/alice_1.txt alice_texts/alice_2.txt alice_texts/alice_3.txt | ./mapper.py | wc -l > tests/test_pairs_count.txt
