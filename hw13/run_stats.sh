#!/usr/bin/env bash

cat alice_pairs/part-00000 alice_pairs/part-00001 alice_pairs/part-00002 | sort -r -n -k 2 | head -n 200 > top_200_pairs.txt
echo $(($(cat alice_pairs_count/part-00000)+$(cat alice_pairs_count/part-00001)+$(cat alice_pairs_count/part-00002))) > pairs_count.txt
