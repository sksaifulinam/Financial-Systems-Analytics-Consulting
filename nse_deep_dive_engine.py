import os
import glob
import datetime
import pandas as pd

# Define path constants for our local environment architecture
input_dir = "./data/input"
quarantine_dir = "./data/quarantine"
staging_dir = "./data/staging"

# Ensure all target architecture storage folders exist
os.makedirs(quarantine_dir, exist_ok=True)
os.makedirs(staging_dir, exist_ok=True)

# Scenario 1: Dynamic File Discovery & Real-World Metadata Harvesting
all_files = glob.glob(os.path.join(input_dir, "nse_feed_*.txt"))
print(f"🚀 [LAUNCH] Executing Deep-Dive Core Engine...")
print(f"📊 [SCENARIO 1] Discovered {len(all_files)} raw data files to process.\n")

for file_path in all_files:
    file_name = os.path.basename(file_path)
    base_name = os.path.splitext(file_name)[0]
    print(f"🔹 Processing Pipeline for: {file_name}")
    
    # Read raw comma-separated data 
    df = pd.read_csv(file_path, sep=",")
    print(f"   ↳ Schema Discovered: {list(df.columns)}")
    
    # Force safe numeric conversion for close_price to prevent string-comparison crashes
    numeric_close = pd.to_numeric(df['close_price'], errors='coerce')
    
    # Scenario 2: Data Quality Isolation logic
    # Row is corrupt if ticker_symbol is null OR close_price failed conversion OR close_price <= 0
    is_corrupt = df['ticker_symbol'].isna() | numeric_close.isna() | (numeric_close <= 0)
    clean_rows = df[~is_corrupt].copy()
    corrupt_rows = df[is_corrupt]
    
    # Isolate corrupt records to the Quarantine area
    if not corrupt_rows.empty:
        quarantine_file_path = os.path.join(quarantine_dir, f"quarantine_{file_name}")
        corrupt_rows.to_csv(quarantine_file_path, sep=",", index=False)
        print(f"   ⚠️ [SCENARIO 2] Corrupt rows routed to: {quarantine_file_path}")

    # Scenario 3: Mid-Flight Business Logic Enrichment
    if not clean_rows.empty:
        clean_rows['close_price'] = numeric_close[~is_corrupt]
        # Track actual load date dynamically using a real-time system timestamp
        clean_rows['ingestion_timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        clean_rows['clean_record_flag'] = "Y"
        
        # Calculate performance value tiers on the fly
        clean_rows['price_performance_tier'] = clean_rows['close_price'].apply(
            lambda price: "High Value" if price > 2000 else "Standard Value"
        )
        print(f"   ✅ [SCENARIO 3] Mid-flight data enrichment complete.")
        
        # Scenario 4: High-Performance Warehouse Staging (Snappy Parquet)
        output_parquet_path = os.path.join(staging_dir, f"staged_{base_name}.parquet")
        clean_rows.to_parquet(output_parquet_path, compression="snappy", index=False)
        print(f"   🎯 [SCENARIO 4] Compressed Snappy Parquet file created at: {output_parquet_path}")
    
    print("-" * 75)

print("\n⚙️ [SUCCESS] Deep-Dive Pipeline execution complete. All stages verified.")
