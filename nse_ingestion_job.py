import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

# STEP 1: Initialize the Master Cloud Ingestion Engines
glueContext = GlueContext(SparkContext.getOrCreate())
spark = glueContext.spark_session

# STEP 2: SOURCE LAYER - Pull the raw pipe-delimited data via the Catalog
# This reads your nse_feed_20260902.txt file seamlessly!
raw_dynamic_frame = glueContext.create_dynamic_frame.from_catalog(
    database = "nse_market_db", 
    table_name = "src_raw_landing"
)

# STEP 3: TRANSFORMATION LAYER - Apply the Data Quality Gatekeeping Filter
# This acts exactly like our Informatica Filter Box! 
# We drop rows where ticker_symbol is 'NULL' or close_price is 0.00
def filter_rows(record):
    if record["ticker_symbol"] == "NULL" or record["ticker_symbol"] is None:
        return False
    if float(record["close_price"]) <= 0:
        return False
    return True

clean_filtered_frame = raw_dynamic_frame.filter(f = filter_rows)

# STEP 4: TARGET LAYER - Stream the clean data into S3 using Parquet format
# This directly optimizes your storage layout to prevent computing lag!
glueContext.write_dynamic_frame.from_options(
    frame = clean_filtered_frame,
    connection_type = "s3",
    connection_options = {
        "path": "s3://saiful-nse-ingestion-engine-2026/archive/"
    },
    format = "parquet"
)
print("NSE Ingestion Pipeline completed successfully with zero error blocks!")
