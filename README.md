# National Stock Exchange (NSE) Market Data Ingestion Engine
 **Project Documentation:** [Main Overview](./ARCHITECTURAL_DEEP_DIVE.md) |  [Architectural Deep-Dive & Local Engine](./ARCHITECTURAL_DEEP_DIVE.md)


## Project Overview
An enterprise-grade cloud data engineering pipeline designed to ingest, clean, and model high-volume relational market datasets from legacy flat-file repositories into an optimized AWS cloud analytics lake. This architecture implements a robust schema-agnostic extraction tier, automated metadata harvesting, mid-flight data validation filters, and a high-performance analytics repository.

## Core Architectural Scenarios Covered
1. **Automated Metadata Discovery:** Programmatic mapping of pipe-delimited flat-file datasets (`nse_feed_YYYYMMDD.txt`) using the AWS Glue Data Catalog framework to eliminate static schema dependencies.
2. **Data Quality Ingestion Quarantine:** Mid-stream Python data-cleansing transformation logic that dynamically intercepts, traps, and purges malformed source payloads (such as empty or corrupted tickers) into an isolated S3 Reject Directory, ensuring zero down-time.
3. **Mid-Flight Business Logic Enrichment:** Downstream column mapping, programmatic type-casting configurations, and auditing column injections to track transaction processing latency.
4. **Columnar Performance Optimization:** Converting uncompressed incoming text records directly into the Apache Parquet storage layer to streamline memory partitioning and eliminate computational skew across analytical target clusters.

## Production Data Pipeline Flow
```text
[ Local Ingestion Layer ] ──> Pipe-Delimited Feeds (.txt) ──> Amazon S3 (raw-landing/)
                                                                    │
                                                                    ▼
[ Compute Transformation Engine ] ◄─────────────────────────── AWS Glue Script
                                                                    │
                     ┌──────────────────────────────────────────────┴──────────────────────────────────────────────┐
                     ▼ (If Data Quality Check FAILS)                                                               ▼ (If Data Quality Check PASSES)
        [ S3 Quarantine Directory ]                                                                  [ Optimized Columnar Target Lake ]
    s3://.../quarantine-reject/                                                                           s3://.../archive/ (Parquet Format)
```

## Technical Tech Stack
* **Storage Tier:** Amazon S3 (Object Storage Layering, Lifecycle Retention Policies)
* **Compute ETL Architecture:** AWS Glue Catalog Workspace, PySpark DataFrames, Schema Mappings
* **Data Optimization:** Apache Parquet Columnar Formatting, Native Metadata Schema Mapping
* **Database & Transformation Scripting:** Advanced Analytical SQL Queries, Python Regular Expressions
