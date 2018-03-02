rm -r ~/hw14/bin/clickstream_reduce_join
rm ~/hw14/pairs-reduce-join.txt
hadoop fs -rm -r /tmp/cs_reduce_join_output

mkdir -p ~/hw14/bin/clickstream_reduce_join/clickstream_extra_classes

javac -classpath /usr/hdp/2.6.4.0-91/hadoop/*:/usr/hdp/2.6.4.0-91/hadoop-mapreduce/* -d ~/hw14/bin/clickstream_reduce_join/clickstream_extra_classes ClickStreamReduceJoin.java

jar -cvf ~/hw14/bin/clickstream_reduce_join/clickstream_reduce_join.jar -C ~/hw14/bin/clickstream_reduce_join/clickstream_extra_classes/ .

hadoop jar ~/hw14/bin/clickstream_reduce_join/clickstream_reduce_join.jar com.larin.ClickStreamReduceJoin /tmp/top-pairs /tmp/all-pairs /tmp/cs_reduce_join_output

hadoop fs -get /tmp/cs_reduce_join_output/part-r-00000 ~/hw14/pairs-reduce-join.txt