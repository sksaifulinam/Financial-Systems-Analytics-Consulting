# ===================================================================
# PROJECT 2: BANKING FRAUD INGESTION & CDC PIPELINE
# FILE NAME: banking_fraud_cdc_job.py
# AUTHOR   : Sk Saiful Inam (Senior Data Lead)
# ===================================================================
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from pyspark.sql.functions import col, max

# Initialize local system contexts
glueContext = GlueContext(SparkContext.getOrCreate())
spark = glueContext.spark_session

# 1. READ TARGET WAREHOUSE BASELINE (Get Max Loaded Date)
# This mimics looking up the last successful watermark timestamp
warehouse_df = glueContext.create_dynamic_frame.from_catalog(
    database="target_market_warehouse", 
    table_name="fact_banking_transactions"
).toDF()

max_load_date = warehouse_df.select(max(col("transaction_date"))).collect()[0][0]

# 2. READ FRESH INCOMING LANDING STREAMS FROM S3
raw_stream_df = spark.read.option("header", "true").csv(
    "s3://global-banking-fraud-lake/landing-zone/daily_transactions/"
)

# 3. APPLY INCREMENTAL CHANGE DATA CAPTURE (CDC) FILTER
# This isolates only the rows that are newer than our warehouse baseline
incremental_delta_df = raw_stream_df.filter(
    col("transaction_date") > max_load_date
)

# 4. OPTIMIZE FOOTPRINT & WRITE OUT IN PARQUET FORMAT
# We save the clean delta records straight to our optimized staging vault
incremental_delta_df.write.mode("append").parquet(
    "s3://global-banking-fraud-lake/silver-zone/isolated_fraud_records/"
)
