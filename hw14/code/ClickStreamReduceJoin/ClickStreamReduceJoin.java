package com.larin;

import java.io.IOException;
import java.util.StringTokenizer;
import java.util.ArrayList;
import java.io.BufferedReader;
import java.io.FileReader;
import java.lang.reflect.Method;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.MultipleInputs;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.input.FileSplit;
import org.apache.hadoop.mapreduce.InputSplit;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;
import org.apache.hadoop.conf.Configured;


public class ClickStreamReduceJoin extends Configured implements Tool {
    private final static String TOP_PAIRS_PREV_FILE_NAME = "top-pairs-12-2017.tsv.gz";
    private final static String ALL_PAIRS_CURR_FILE_NAME = "all-pairs-01-2018.tsv.gz";
    private final static String SEPARATOR = "\t";

    public static class ClickStreamMapper extends Mapper<Object, Text, Text, Text> {
        private Text value = new Text();
        private Text tag = new Text();
        private String fileName;

        public void map(Object key, Text record, Context context) throws IOException, InterruptedException {
            String[] parts = record.toString().split(SEPARATOR); // Делим строку на токены "prev curr type n" -> "prev" "curr" "type" "n"
            tag.set(parts[0].trim() + " " + parts[1].trim()); // Устанавливаем ключ "prev curr"
            value.set(parts[3].trim() + SEPARATOR + fileName); // Устанавливаем количество кликов с идентификатором файла "n\tfile_name"
            context.write(tag, value); // Пишем ключ-значение в контекст
        }

        @Override
        protected void setup(Context context) throws IOException, InterruptedException {
            // Вся эта магия по извлечению имени файла взята отсюда:
            // https://stackoverflow.com/questions/11130145/hadoop-multipleinputs-fails-with-classcastexception
            InputSplit split = context.getInputSplit();
            Class<? extends InputSplit> splitClass = split.getClass();
            FileSplit fileSplit = null;
            if (splitClass.equals(FileSplit.class)) {
                fileSplit = (FileSplit) split;
            } else if (splitClass.getName().equals("org.apache.hadoop.mapreduce.lib.input.TaggedInputSplit")) {
                try {
                    Method getInputSplitMethod = splitClass.getDeclaredMethod("getInputSplit");
                    getInputSplitMethod.setAccessible(true);
                    fileSplit = (FileSplit) getInputSplitMethod.invoke(split);
                } catch (Exception e) {
                    throw new IOException(e);
                }
            }
            fileName = fileSplit.getPath().getName();
        }
    }

    // Сейчас данные на редьюсер приходят отсортированные по ключу, но в случайном порядке:
    // key1 file_prev
    // key1 file_curr
    // key2 file_curr
    // key2 file_prev
    // В идеале, надо осуществлять промежуточную сортировку, чтобы второй файл всегда шел за первым:
    // key1 file_prev
    // key1 file_curr
    // key2 file_prev
    // key2 file_curr
    // Тогда можно было бы обойтись без промежуточного буфера, но так как данных на редьюсер приходит немного,
    // то можно ограничиться и текущим вариантом
    public static class ClickStreamReducer extends Reducer<Text, Text, Text, Text> {
        private Text result = new Text();

        public void reduce(Text key, Iterable<Text> values, Context context) throws IOException, InterruptedException {
            Boolean status = false;
            ArrayList<String> buffer = new ArrayList<String>(); // Используем массив для добавления пар за второй месяц на случай, если пар будет больше одной

            for (Text val : values) {
                String[] parts = val.toString().split(SEPARATOR); // Разбиваем входящее значение на количество и идентификатор файла "n\tfile_name" -> "n" "file_name"
                if (parts[1].equals(TOP_PAIRS_PREV_FILE_NAME)) { // Если имя файла совпадает с первым файлом, где топ 10000 записей
                    status = true; // Устанавливаем флаг, что пары за первый и второй месяц совпадают
                } else {
                    buffer.add(parts[0]); // Добавляем пары за второй месяц в буфер
                }
            }

            if (buffer.size() > 0 && status == true) { // Если за первый и второй месяц пришла хотя бы одна пара
                for (String buf : buffer) { // Итерируемся через записи в буфере и выводим результат
                    result.set(buf);
                    context.write(key, result);
                }
            }
        }
    }

    public static void main(String[] args) throws Exception {
        int res = ToolRunner.run(new ClickStreamReduceJoin(), args);
        System.exit(res);
    }

    public int run(String[] args) throws Exception {
        Job job = Job.getInstance(getConf(), ClickStreamReduceJoin.class.getCanonicalName());

        job.setJarByClass(ClickStreamReduceJoin.class);
        job.setReducerClass(ClickStreamReducer.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(Text.class);

        MultipleInputs.addInputPath(job, new Path(args[0]), TextInputFormat.class, ClickStreamMapper.class);
        MultipleInputs.addInputPath(job, new Path(args[1]), TextInputFormat.class, ClickStreamMapper.class);

        FileOutputFormat.setOutputPath(job, new Path(args[2]));

        return job.waitForCompletion(true) ? 0 : 1;
    }
}
