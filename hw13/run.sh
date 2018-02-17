#!/usr/bin/env bash

/bin/hadoop jar /usr/hdp/current/hadoop-mapreduce-client/hadoop-streaming.jar \
    -input /alice_texts/* \
    -output /data/word_count/alice_texts_result \
    -mapper 'mapper.py' \
    -reducer 'reducer.py' \
    -file mapper.py \
    -file reducer.py