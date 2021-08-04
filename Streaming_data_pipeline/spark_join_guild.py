#!/usr/bin/env python
"""Extract events from kafka and write them to hdfs
"""
import json
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, from_json
from pyspark.sql.types import StructType, StructField, StringType

# Create a function to define the schema of join guild
def join_guild_event_schema():
    """
    root
    |-- Accept: string (nullable = true)
    |-- Host: string (nullable = true)
    |-- User-Agent: string (nullable = true)
    |-- event_type: string (nullable = true)
    |-- name: string (nullable = true)
    """
    return StructType([
        StructField("Accept", StringType(), True),
        StructField("Host", StringType(), True),
        StructField("User-Agent", StringType(), True),
        StructField("event_type", StringType(), True),
        StructField("name", StringType(), True),
    ])

# Create a function to filter events of users joining guilds 
@udf('boolean')
def is_join_guild(event_as_json):
    """udf for filtering events
    """
    event = json.loads(event_as_json)
    if (event['event_type'] == 'join_guild'):
        return True
    return False


def main():
    """main
    """
    spark = SparkSession \
        .builder \
        .appName("ExtractEventsJob") \
        .enableHiveSupport() \
        .getOrCreate()

    raw_events = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "kafka:29092") \
        .option("subscribe", "events") \
        .load()
    
    join_guild = raw_events \
        .filter(is_join_guild(raw_events.value.cast('string'))) \
        .select(raw_events.value.cast('string').alias('raw_event'),
                raw_events.timestamp.cast('string'),
                from_json(raw_events.value.cast('string'),
                          join_guild_event_schema()).alias('json')) \
        .select('raw_event', 'timestamp', 'json.*')

    spark.sql("drop table if exists join_guild")
    sql_string = """
        create external table if not exists join_guild (
            raw_event string,
            timestamp string,
            Accept string,
            Host string,
            `User-Agent` string,
            event_type string,
            name string
            )
            stored as parquet
            location '/tmp/join_guild'
            tblproperties ("parquet.compress"="SNAPPY")
            """
    spark.sql(sql_string)

    sink = join_guild \
        .writeStream \
        .format("parquet") \
        .option("checkpointLocation", "/tmp/checkpoints_for_join_guild") \
        .option("path", "/tmp/join_guild") \
        .trigger(processingTime="10 seconds") \
        .start()

    sink.awaitTermination()


if __name__ == "__main__":
    main()
