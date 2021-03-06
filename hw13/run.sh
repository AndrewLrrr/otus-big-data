#!/usr/bin/env bash

/usr/bin/hadoop jar /usr/hdp/current/hadoop-mapreduce-client/hadoop-streaming.jar \
    -D mapred.reduce.tasks=3 \
    -input /tmp/words-count/alice_texts \
    -output /tmp/words-count/alice_pairs \
    -mapper 'python3 mapper.py' \
    -reducer 'python3 reducer.py' \
    -file mapper.py \
    -file reducer.py
