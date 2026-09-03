# NSE Market Data Ingestion Engine: Deep-Dive Blueprint

 **Project Documentation:** [Main Overview](./README.md) |  [Architectural Deep-Dive & Local Engine](./ARCHITECTURAL_DEEP_DIVE.md)

This document outlines the resilient production engineering patterns used to build a complete end-to-end market data ingestion lifecycle with zero error boundaries.

---

##  The 4 Master Project Scenarios Covered

### 1. Scenario 1: Automated Metadata Harvesting
- Automatically discovers dynamic incoming daily text files (`data/input/nse_feed_*.txt`).
- Dynamically extracts internal schemas (`['ticker_symbol', 'trade_date', 'close_price', 'account_status']`) mid-flight.

### 2. Scenario 2: Data Quality Isolation Layer
- Enforces strict type-coercion validation to gracefully catch unexpected text string data inside numeric fields.
- Routes corrupt records instantly to an isolated `data/quarantine/` directory to prevent pipeline crashes.

### 3. Scenario 3: Mid-Flight Business Logic Enrichment
- Dynamically injects an `ingestion_timestamp` metric to track the exact load time automatically.
- Applies automated clean record metadata flags (`clean_record_flag = Y`).
- Computes custom business metrics on the fly (e.g., categorizing records into `High Value` or `Standard Value`).

### 4. Scenario 4: High-Performance Warehouse Staging
- Converts processed datasets directly into optimized Apache Parquet format.
- Applies Snappy compression metrics to minimize analytics warehouse compute and storage overhead in `data/staging/`.

---

##  Complete End-to-End Component Directory

The master framework is structured into a professional, modular three-tier layout:

### 1. The Orchestration Layer (`run_pipeline.sh`)
- A production-grade Bash shell wrapper that automates the workspace setup.
- Checks data directory health, executes the core processing logic, and prints a full data lineage audit log upon completion.

### 2. The Processing Engine (`nse_deep_dive_engine.py`)
- The core Python data processing script that executes all schema extractions, type coercions, data quality filters, and Snappy Parquet generation routines.

### 3. The Target Data Warehouse Layer (`warehouse_ddl_mapping.sql`)
- The analytics staging layer designed for cloud environments like AWS Redshift or enterprise PostgreSQL.
- Implements a production table (`nse_market_data_fact`) and an optimized reporting view (`vw_high_value_tickers`) for business intelligence tooling.

---

##  Storage Architecture Blueprint
- **`data/input/`** : Ingest entry point for daily text data feeds.
- **`data/quarantine/`** : Isolation vault for corrupted row metrics.
- **`data/staging/`** : High-performance warehouse staging target for compressed Parquet outputs.
