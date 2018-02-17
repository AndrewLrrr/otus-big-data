#!/usr/bin/env bash

cat alice.txt | ./mapper.py | sort | ./reducer.py | sort -rk 2 | head -n 30