package com.larin;

import java.io.IOException;
import java.util.StringTokenizer;
import java.util.HashSet;
import java.net.URI;
import java.io.BufferedReader;
import java.io.FileReader;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;
import org.apache.hadoop.conf.Configured;


public class ClickStreamBroadcastJoin extends Configured implements Tool {
    private final static String SEPARATOR = "\t";

    public static class ClickStreamMapper extends Mapper<Object, Text, Text, Text> {
        private Text outKey = new Text();
        private Text outValue = new Text();
        private HashSet<String> cache = new HashSet<String>();
        private String keyPair = null;

        public void map(Object key, Text record, Context context) throws IOException, InterruptedException {
            String[] parts = record.toString().split(SEPARATOR); // Делим строку на токены "prev curr type n" -> "prev" "curr" "type" "n"
            keyPair = parts[0].trim() + " " + parts[1].trim();
            if (cache.contains(keyPair)) { // Если ключ есть в кеше, то отправляем значение на редьюсер
                outKey.set(keyPair);
                outValue.set(parts[3].trim()); // Устанавливаем количество кликов "n"
                context.write(outKey, outValue);
            }
        }

        @Override
        protected void setup(Context context) throws IOException, InterruptedException {
            try {
                URI[] cacheFiles = context.getCacheFiles();
                if(cacheFiles != null && cacheFiles.length > 0) {
                    for(URI cacheFile : cacheFiles) {
                        readFile(new Path(cacheFile.getPath()));
                    }
                }
            } catch(IOException ex) {
                System.err.println("Exception in mapper setup: " + ex.getMessage());
            }
        }

        private void readFile(Path filePath) {
            try {
                BufferedReader bufferedReader = new BufferedReader(new FileReader(filePath.getName().toString()));
                String buffer = null;
                // Читаем файл и сохраняем ключи в память
                while((buffer = bufferedReader.readLine()) != null) {
                    String[] parts = buffer.split(SEPARATOR); // Делим строку на токены "prev curr type n" -> "prev" "curr" "type" "n"
                    cache.add(parts[0].trim() + " " + parts[1].trim()); // Устанавливаем ключ по которому будем осуществлять Join - "prev curr"
                }
            } catch(IOException ex) {
                System.err.println("Exception while reading file in memory: " + ex.getMessage());
            }
        }
    }

    public static class ClickStreamReducer extends Reducer<Text, Text, Text, Text> {
        // Do nothing...
    }

    public static void main(String[] args) throws Exception {
        int res = ToolRunner.run(new ClickStreamBroadcastJoin(), args);
        System.exit(res);
    }

    public int run(String[] args) throws Exception {
        Job job = Job.getInstance(getConf(), ClickStreamBroadcastJoin.class.getCanonicalName());

        job.setJarByClass(ClickStreamBroadcastJoin.class);
        job.setMapperClass(ClickStreamMapper.class);
        job.setReducerClass(ClickStreamReducer.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(Text.class);

        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));

        job.addCacheFile(new Path(args[2]).toUri());
        return job.waitForCompletion(true) ? 0 : 1;
    }
}