import os
import sys
import re
import time

from pyspark.sql import functions as F
from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf,col
from pyspark.sql.types import StringType, FloatType, StructType, TimestampType

# import seaborn as sns

os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable
PERIOD =10

spark = SparkSession \
    .builder \
    .appName("structured") \
    .config("spark.sql.streaming.forceDeleteTempCheckpointLocation", True) \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

schemas = StructType().add('Date',TimestampType()).add('name','string').add('text','string').add('media','string')
parquet_sdf = spark.readStream.schema(schemas).format('parquet').load('dfs\Data_for_{PERIOD}_sec_at20231223015422.parquet')

print(parquet_sdf.isStreaming)
print(parquet_sdf.schema)
co = parquet_sdf.groupBy('name').count()
query = co \
    .writeStream \
    .outputMode("complete") \
    .format("console") \
    .option("truncate", "false") \
    .start()
query.awaitTermination()