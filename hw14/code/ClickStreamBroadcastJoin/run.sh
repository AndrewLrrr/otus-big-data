#!/usr/bin/env bash

rm -r ~/hw14/bin/clickstream_broadcast_join
rm ~/hw14/pairs-broadcast-join.txt
hadoop fs -rm -r /tmp/cs_broadcust_join_output

mkdir -p ~/hw14/bin/clickstream_broadcast_join/classes

javac -classpath /usr/hdp/2.6.4.0-91/hadoop/*:/usr/hdp/2.6.4.0-91/hadoop-mapreduce/* -d ~/hw14/bin/clickstream_broadcast_join/classes ClickStreamBroadcastJoin.java

jar -cvf ~/hw14/bin/clickstream_broadcast_join/clickstream_broadcast_join.jar -C ~/hw14/bin/clickstream_broadcast_join/classes/ .

hadoop jar ~/hw14/bin/clickstream_broadcast_join/clickstream_broadcast_join.jar com.larin.ClickStreamBroadcastJoin /tmp/all-pairs /tmp/cs_broadcust_join_output /tmp/top-pairs-for-cache/top-pairs-12-2017.tsv

hadoop fs -get /tmp/cs_broadcust_join_output/part-r-00000 ~/hw14/pairs-broadcast-join.txt