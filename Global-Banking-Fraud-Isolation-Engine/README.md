>  **ENTERPRISE CORE ARTIFACT SPECS**
> * **FOLDER REPOSITORY:** `Global-Banking-Fraud-Isolation-Engine`
> * **FILE DEPLOYMENT:** `README.md`
> * **AUTHOR DATA LEAD:** **Sk Saiful Inam (Senior Data Lead)**
> * **CORE RUNTIME TARGET:** Enterprise Cloud Data Pipeline for Ingestion, Deduplication, and Fraud Isolation

# Global Banking Fraud Isolation Engine

## Project Overview
An enterprise-grade cloud migration data pipeline designed to ingest, clean, deduplicate, and model high-volume transactional banking data streams from legacy on-premise systems into an optimized AWS analytical data warehouse. This engine serves as a secure validation barrier, automatically trapping, scoring, and routing anomalous or fraudulent transaction rows into a quarantine layer mid-flight.

##  Production Architecture & Data Flow Map

```text
[  Legacy Core Bank Database ]
        │ (Teradata On-Prem Ledger Dumps)
        ▼
[  AWS S3 Landing Zone ] ──────► daily_ledger.csv (Raw Input Tier)
                                        │
                                        ▼  (Spark Ingestion Lookup)
                                 [ ⚙️ AWS Glue / PySpark Compute Engine ]
                                        │
        ┌───────────────────────────────┴───────────────────────────────┐
        ▼ (If Dynamic Fraud Score > 0.90 OR Account Number IS NULL)      ▼ (If Record Is Verified Clean & Unique)
[  S3 Quarantine Zone ]                                        [  S3 Silver Zone Staging Vault ]
  quarantine_zone/flagged_data.csv                                silver_zone/clean_data.csv
  (Isolated for Compliance Audit)                                 (Stored in Columns For Analytics)
                                                                        │
                                                                        ▼ (COPY Parallel Bulk Load)
                                                                 [  Target Data Warehouse ]
                                                                   Amazon Redshift Fact Tables
                                                                   (Distribution/Sort Key Optimized)
```

## Core Architectural Scenarios Covered
1. **Automated High-Watermark CDC:** Programmatically queries the target reporting warehouse table to calculate the maximum transaction date in memory, using it as a dynamic variable to extract only fresh incremental delta rows from the storage lakes.
2. **Analytical Window Deduplication:** Leverages PySpark memory partitions and `Window.partitionBy` functions to look for network retry anomalies, purging identical, stale duplicate transaction records mid-flight.
3. **Automated Risk Isolation Quarantine:** Deploys a conditional safety barrier that intercepts corrupted payloads or high-volatility financial rows (Fraud Score > 0.90), routing them safely into an isolated storage directory before they hit analytical layers.
4. **Data Skew Cluster Balancing:** Mitigates Out-Of-Memory cluster processing crashes by applying a programmatic Data Salting technique, appending random keys across heavy transaction accounts to balance compute nodes evenly.

## Technical Tech Stack
* **Storage Infrastructure:** Amazon S3 (Multi-Tier Object Storage, Fine-Grained IAM Policies)
* **Compute Processing Core:** AWS Glue Serverless Framework, Apache Spark (PySpark Engine API)
* **Data Lakehouse Modeling:** Columnar Architecture, Dimensional Star Schemas, Automated Watermarking
* **Language & Analysis Tools:** Advanced Analytical SQL, Python Data Engineering Libraries (Pandas/PySpark)
