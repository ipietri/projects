#!/usr/bin/env python
"""Extract events from kafka and write them to hdfs
"""
import json
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, from_json
from pyspark.sql.types import StructType, StructField, StringType

# Create a function to define the schema of weapon purchases
# All weapon purchases have the same schema
def purchase_weapon_event_schema():
    """
    root
    |-- Accept: string (nullable = true)
    |-- Host: string (nullable = true)
    |-- User-Agent: string (nullable = true)
    |-- event_type: string (nullable = true)
    |-- type: string (nullable = true)
    """
    return StructType([
        StructField("Accept", StringType(), True),
        StructField("Host", StringType(), True),
        StructField("User-Agent", StringType(), True),
        StructField("event_type", StringType(), True),
        StructField("type", StringType(), True),
    ])

# Create a function to filter weapon purchases 
@udf('boolean')
def is_weapon_purchase(event_as_json):
    """udf for filtering events
    """
    event = json.loads(event_as_json)
    if (event['event_type'] == 'purchase_sword') or (event['event_type'] == 'purchase_crossbow') \
    or (event['event_type'] == 'purchase_shield'):
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

    weapon_purchases = raw_events \
        .filter(is_weapon_purchase(raw_events.value.cast('string'))) \
        .select(raw_events.value.cast('string').alias('raw_event'),
                raw_events.timestamp.cast('string'),
                from_json(raw_events.value.cast('string'),
                          purchase_weapon_event_schema()).alias('json')) \
        .select('raw_event', 'timestamp', 'json.*')

    spark.sql("drop table if exists weapon_purchases")
    sql_string = """
        create external table if not exists weapon_purchases (
            raw_event string,
            timestamp string,
            Accept string,
            Host string,
            `User-Agent` string,
            event_type string,
            type string
            )
            stored as parquet
            location '/tmp/weapon_purchases'
            tblproperties ("parquet.compress"="SNAPPY")
            """
    spark.sql(sql_string)

    sink = weapon_purchases \
        .writeStream \
        .format("parquet") \
        .option("checkpointLocation", "/tmp/checkpoints_for_weapon_purchases") \
        .option("path", "/tmp/weapon_purchases") \
        .trigger(processingTime="10 seconds") \
        .start()

    sink.awaitTermination()

if __name__ == "__main__":
    main()
