# NSE Market Data Ingestion Engine: Deep-Dive Blueprint
 **Project Documentation:** [Main Overview](./README.md) |  [Architectural Deep-Dive & Local Engine](./README.md)


This document serves as our deep-dive technical blueprint. It outlines the resilient engineering patterns used to process raw market data feeds with zero error boundaries.

---

## 🏗️ The 4 Master Project Scenarios Covered

### 1. Scenario 1: Automated Metadata Harvesting
- Automatically discovers dynamic incoming data targets (`nse_feed_*.txt`).
- Dynamically extracts internal schemas (`['ticker_symbol', 'trade_date', 'close_price', 'account_status']`) on flight.

### 2. Scenario 2: Data Quality Isolation Layer
- Enforces strict type-coercion validation to gracefully catch unexpected text string data inside numeric fields.
- Routes corrupt records instantly to an isolated `/data/quarantine/` directory to prevent pipeline crashes.

### 3. Scenario 3: Mid-Flight Business Logic Enrichment
- Dynamically injects an `ingestion_timestamp` metric to track the exact load time.
- Applies automated clean record metadata flags (`clean_record_flag = Y`).
- Computes custom business metrics on the fly (e.g., categorizing records into `High Value` or `Standard Value`).

### 4. Scenario 4: High-Performance Warehouse Staging
- Converts processed datasets directly into optimized Apache Parquet format.
- Applies Snappy compression metrics to minimize analytics warehouse compute and storage overhead.

---

## 📁 Storage Layer Blueprint
- **`/data/input/`** : Ingest point for daily text feeds.
- **`/data/quarantine/`** : Isolation vault for corrupted row metrics.
- **`/data/staging/`** : High-performance target for compressed Parquet outputs.
