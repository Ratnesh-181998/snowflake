from pyspark.sql import SparkSession
from pyspark.sql.functions import *

# Initialize a SparkSession
spark = SparkSession.builder \
    .appName("SnowflakeDataRead") \
    .config("spark.jars", "gs://jars-gds/spark-snowflake_2.12-2.12.0-spark_3.3.jar,gs://jars-gds/snowflake-jdbc-3.13.30.jar") \
    .getOrCreate()

# Snowflake connection options
sfOptions = {
    "sfURL": "https://uiioyzf-vr10915.snowflakecomputing.com",
    "sfAccount": "uiioyzf-vr10915",
    "sfUser": "gds",
    "sfPassword": "Gds@@2023",
    "sfDatabase": "GCS_SNOWPIPE",
    "sfSchema": "PUBLIC",
    "sfWarehouse": "COMPUTE_WAREHOUSE",
    "sfRole": "ACCOUNTADMIN"
}

SNOWFLAKE_SOURCE_NAME = "net.snowflake.spark.snowflake"

# Read data from Snowflake
df = spark.read \
    .format(SNOWFLAKE_SOURCE_NAME) \
    .options(**sfOptions) \
    .option("dbtable", "SNOWPIPE") \
    .load()

# Show the data (for testing purposes)
df.show()

# Filter for 'Completed' orders
completed_orders_df = df.filter(col("order_status") == "Completed")

# Write the filtered data to Snowflake (new table: completed_orders)
completed_orders_df.write \
    .format(SNOWFLAKE_SOURCE_NAME) \
    .options(**sfOptions) \
    .option("dbtable", "completed_orders") \
    .mode("append") \
    .save()

print("Data write successful in target table !!")

# Stop the SparkSession
spark.stop()