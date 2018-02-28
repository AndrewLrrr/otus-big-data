package org.myorg;

import java.io.IOException;
import java.util.StringTokenizer;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;
import org.apache.hadoop.conf.Configured;
import java.util.HashSet;
import java.net.URI;
import java.io.BufferedReader;
import java.io.FileReader;

public class ClickStreamBroadcastJoin extends Configured implements Tool {

    public static class ClickStreamMapper extends Mapper<Object, Text, Text, IntWritable> {

        private IntWritable count = new IntWritable();
        private Text tag = new Text();
        private final static String separator = "\t";

        private HashSet<String> stopWords = new HashSet<String>();

        public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
            String[] parts = value.toString().split(separator);
            if(!stopWords.contains(parts[2].trim())) {
                tag.set(parts[2].trim());
                count.set(Integer.parseInt(parts[3]));
                context.write(tag, count);
            }
        }

        @Override
        protected void setup(Context context) throws IOException, InterruptedException {
            try{
                URI[] stopWordsFiles = context.getCacheFiles();
                if(stopWordsFiles != null && stopWordsFiles.length > 0) {
                    for(URI stopWordFile : stopWordsFiles) {
                        readFile(new Path(stopWordFile.getPath()));
                    }
                }
            } catch(IOException ex) {
                System.err.println("Exception in mapper setup: " + ex.getMessage());
            }
        }

        private void readFile(Path filePath) {
            try{
                BufferedReader bufferedReader = new BufferedReader(new FileReader(filePath.getName().toString()));
                String stopWord = null;
                while((stopWord = bufferedReader.readLine()) != null) {
                    stopWords.add(stopWord.trim().toLowerCase());
                }
            } catch(IOException ex) {
                System.err.println("Exception while reading stop words file: " + ex.getMessage());
            }
        }
    }

    public static class IntSumReducer extends Reducer<Text, IntWritable, Text, IntWritable> {
        private IntWritable result = new IntWritable();

        public void reduce(Text key, Iterable<IntWritable> values, Context context) throws IOException, InterruptedException {
            int sum = 0;
            for (IntWritable val : values) {
                sum += val.get();
            }
            result.set(sum);
            context.write(key, result);
        }
    }

    public static void main(String[] args) throws Exception {
        int res = ToolRunner.run(new ClickStreamExtra(), args);
        System.exit(res);
    }

    public int run(String[] args) throws Exception {
        Job job = Job.getInstance(getConf(), ClickStreamExtra.class.getCanonicalName());

        job.setJarByClass(ClickStreamExtra.class);
        job.setMapperClass(ClickStreamMapper.class);
        job.setCombinerClass(IntSumReducer.class);
        job.setReducerClass(IntSumReducer.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(IntWritable.class);

        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));

        job.addCacheFile(new Path(args[2]).toUri());
        return job.waitForCompletion(true) ? 0 : 1;
    }
}