#!/usr/bin/env bash

/usr/bin/hadoop jar /usr/hdp/current/hadoop-mapreduce-client/hadoop-streaming.jar \
    -D mapred.reduce.tasks=3 \
    -input /tmp/words-count/alice_texts \
    -output /tmp/words-count/alice_pairs_count \
    -mapper 'python3 mapper.py' \
    -reducer '/usr/bin/wc -l' \
    -file mapper.py
