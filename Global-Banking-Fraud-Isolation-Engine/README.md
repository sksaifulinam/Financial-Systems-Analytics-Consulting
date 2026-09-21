=================================================================================
PROJECT LOGBOOK: Global Banking Fraud Isolation Engine
REPOSITORY FOLDER NAME: Global-Banking-Fraud-Isolation-Engine
[SYSTEM SUMMARY]
This cloud data engine modernizes legacy financial pipeline layers by moving heavy transaction processing from on-premise transactional databases into scalable cloud environments.
The infrastructure automates the ingestion, validation, and risk-routing of daily high-volume credit card and retail banking data streams.
[CORE ARCHITECTURE STEPS]
Change Data Capture (CDC): Intercepts daily source files incrementally by running a watermark lookup against the maximum transaction date already saved in our target warehouse layer.
Mid-Flight Deduplication: Leverages PySpark window analytical functions to look for communication retries and drop identical, stale rows instantly based on transaction IDs.
Risk Quarantine Isolation: Runs conditional validation barriers to filter out malformed files or high-risk records (Fraud Score > 0.90) and route them safely into an isolated S3 quarantine folder before they hit reporting tools.
Parquet Compaction: Packages the validated datasets into compressed Apache Parquet formats to optimize storage space and accelerate database search speeds.
[INFRASTRUCTURE BLUEPRINT]
Raw File Feeds: Comma-Separated Values (.csv) daily ledger dumps
Compute & Integration Engine: AWS Glue running PySpark frameworks
Secure Storage Lake: Amazon Simple Storage Service (S3) multi-tier layout
Target Analytical Destination: Amazon Redshift Data Warehouse Cluster
