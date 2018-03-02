rm -rf ~/hw14/bin/clickstream_reduce_join

hadoop fs -rm -r /tmp/cs_reduce_join_output

mkdir -p ~/hw14/bin/clickstream_reduce_join/clickstream_extra_classes

javac -classpath /usr/hdp/2.6.4.0-91/hadoop/*:/usr/hdp/2.6.4.0-91/hadoop-mapreduce/* -d ~/hw14/bin/clickstream_reduce_join/clickstream_extra_classes ClickStreamReduceJoin.java

jar -cvf ~/hw14/bin/clickstream_reduce_join/clickstream_reduce_join.jar -C ~/hw14/bin/clickstream_reduce_join/clickstream_extra_classes/ .

hadoop jar ~/hw14/bin/clickstream_reduce_join/clickstream_reduce_join.jar com.larin.ClickStreamReduceJoin /tmp/top-pairs /tmp/all-pairs /tmp/cs_reduce_join_output
