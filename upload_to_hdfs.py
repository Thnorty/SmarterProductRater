from pyspark.sql import SparkSession
import os
os.environ["SPARK_HOME"] = r"C:\Program Files\Spark\spark-3.5.5-bin-hadoop3"

# Initialize Spark Session
spark = SparkSession.builder \
    .appName("ProductRatingAnalysis") \
    .config("spark.hadoop.fs.defaultFS", "hdfs://localhost:3501") \
    .getOrCreate()

# First, read your JSONL file
local_file_path = "file:///C:/Users/otota/Documents/TOBB ETÜ Homeworks/BİL 401/Project/datas/appliances/appliances_with_sentiment_score_and_is_spam.jsonl"
df = spark.read.json(local_file_path)

# Define your output path in HDFS
output_path = "/datas/appliances/appliances_with_sentiment_score_and_is_spam.parquet"

# Write the DataFrame as Parquet to HDFS
df.write.mode("overwrite").parquet(output_path)

print(f"Successfully saved Parquet files to HDFS at {output_path}")

# List files in the output directory
hadoop_fs = spark._jvm.org.apache.hadoop.fs.FileSystem.get(spark._jsc.hadoopConfiguration())
path = spark._jvm.org.apache.hadoop.fs.Path(output_path)
file_status = hadoop_fs.listStatus(path)

print("Files in output directory:")
for status in file_status:
    print(status.getPath().getName())
