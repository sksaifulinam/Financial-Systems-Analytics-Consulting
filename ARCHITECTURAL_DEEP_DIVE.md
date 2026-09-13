# NSE Market Data Ingestion Engine: Deep-Dive Blueprint

📂 **Project Documentation:** [Main Overview](./README.md) | 🔬 [Architectural Deep-Dive & Local Engine](./ARCHITECTURAL_DEEP_DIVE.md)

This document maps out the production-grade data engineering patterns used to process daily National Stock Exchange (NSE) End-of-Day (EOD) Bhavcopy market feeds with absolute zero-error boundaries.

---

## 🏗️ Production Architecture & Data Flow Map

```text
[1. SOURCE LAYER]         -->  [2. ORCHESTRATION LAYER]   -->  [3. CORE PROCESSING TIER]
Daily EOD Bhavcopy Feeds       run_pipeline.sh                 nse_deep_dive_engine.py
Raw Flat Files (.txt/.csv)     (Unix Bash Wrapper Engine)      (Python 3 / Pandas DataFrames)
                                                                             |
                                     +---------------------------------------+
                                     | (Defensive Type Coercion Validation Check)
                                     |
                                     +---> [IF NULL / CORRUPT DATA] ---> [4. QUARANTINE VAULT]
                                     |                                   data/quarantine/quarantine_*.txt
                                     |
                                     +---> [IF CLEAN DATA METRIC]   ---> [5. HIGH-PERFORMANCE STAGING]
                                                                         data/staging/staged_*.parquet
                                                                         (Snappy Columnar Compression)
                                                                                     |
                                                                                     v
                                                                        [6. TARGET WAREHOUSE LAYER]
                                                                         AWS Redshift Fact Tables
                                                                         (warehouse_ddl_mapping.sql)
```

---

## 🔬 The 4 Master Project Scenarios Covered

### 1. Scenario 1: Automated Metadata Harvesting
- **Operation:** Dynamically discovers daily incoming text file targets (`data/input/nse_feed_*.txt`) matching exchange patterns.
- **Output:** Extracts and harvests structural field layouts (`['ticker_symbol', 'trade_date', 'close_price', 'account_status']`) mid-flight without relying on fixed index assumptions.

### 2. Scenario 2: Data Quality Isolation Layer (The Quarantine Path)
- **Operation:** Enforces strict type-coercion using `pd.to_numeric(errors='coerce')` to catch unexpected text strings in numeric fields.
- **Output:** Automatically strips out rows with missing ticker names or invalid closing prices (`<= 0`). Routes them instantly to an isolated `data/quarantine/` reject vault to protect downstream database integrity.

### 3. Scenario 3: Mid-Flight Business Logic Enrichment
- **Operation:** Dynamically injects an `ingestion_timestamp` metric to track the exact runtime execution lineage.
- **Output:** Appends automated audit validation quality flags (`clean_record_flag = Y`) and runs a performance tier category rule (`close_price > 2000` ? `"High Value"` : `"Standard Value"`).

### 4. Scenario 4: High-Performance Warehouse Staging
- **Operation:** Converts clean, validated records into high-performance Apache Parquet format.
- **Output:** Applies Snappy columnar compression engines to minimize data warehouse compute costs and optimize historical query execution speeds.

---

## 🛠️ Complete Structural Architecture Index

- **Orchestration Layer (`run_pipeline.sh`):** A Unix Bash script that audits directory structures, executes the core python pipeline payload, monitors exit status codes (`$?`), and prints terminal logging summaries.
- **Processing Core (`nse_deep_dive_engine.py`):** The computational engine using Python 3 and Pandas dataframes to execute type conversions, logic splits, and Parquet serialization.
- **Target Storage Layer (`warehouse_ddl_mapping.sql`):** The analytics relational warehouse schema mapping defining production fact tables (`nse_market_data_fact`) and operational views for reporting utilities.
