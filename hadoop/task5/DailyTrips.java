import java.io.IOException;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class DailyTrips {
  public static class M extends Mapper<LongWritable, Text, Text, Text> {
    private final Text k = new Text();
    private final Text v = new Text();
    @Override
    protected void map(LongWritable key, Text value, Context ctx) throws IOException, InterruptedException {
      String[] f = value.toString().split(",");
      if (f.length < 10 || f[0].equals("pickup_datetime")) return;
      try { Double.parseDouble(f[3]); } catch (NumberFormatException e) { return; }
      k.set(f[9]);
      v.set(f[3] + ",1");
      ctx.write(k, v);
    }
  }
  public static class R extends Reducer<Text, Text, Text, Text> {
    @Override
    protected void reduce(Text key, Iterable<Text> vals, Context ctx) throws IOException, InterruptedException {
      long cnt = 0; double tot = 0;
      for (Text t : vals) {
        String[] p = t.toString().split(",");
        tot += Double.parseDouble(p[0]);
        cnt += Long.parseLong(p[1]);
      }
      ctx.write(key, new Text(cnt + "\t" + String.format("%.3f", tot / cnt)));
    }
  }
  public static void main(String[] args) throws Exception {
    Job job = Job.getInstance(new Configuration(), "daily trips");
    job.setJarByClass(DailyTrips.class);
    job.setMapperClass(M.class);
    job.setReducerClass(R.class);
    job.setOutputKeyClass(Text.class);
    job.setOutputValueClass(Text.class);
    FileInputFormat.addInputPath(job, new Path(args[0]));
    FileOutputFormat.setOutputPath(job, new Path(args[1]));
    System.exit(job.waitForCompletion(true) ? 0 : 1);
  }
}
