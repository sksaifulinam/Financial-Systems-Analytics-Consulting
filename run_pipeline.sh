#!/bin/bash
# ==============================================================================
# PROJECT    : NSE-MarketData-Ingestion-Engine
# COMPONENTS : Unix Automation Shell Wrapper (Data Management & Orchestration)
# AUTHOR     : Sk Saiful Inam (Senior Data Lead)
# ==============================================================================

INPUT_DIR="./data/input"
QUARANTINE_DIR="./data/quarantine"
STAGING_DIR="./data/staging"

echo "======================================================================"
echo "🏁 [SH-WRAPPER] Starting Master End-to-End Orchestration Flow..."
echo "======================================================================"

# Step 1: Verify Directory Foundations
echo "Step 1: Auditing storage workspace layout..."
if [ ! -d "$INPUT_DIR" ]; then
    echo " Error: Source input directory '$INPUT_DIR' does not exist."
    exit 1
fi
echo " Directory audit complete. Found input data layer."

# Step 2: Kick off the Core Processing Python Engine
echo "Step 2: Launching Python Processing Engine Core..."
python nse_deep_dive_engine.py
if [ $? -ne 0 ]; then
    echo " Pipeline Ingestion Failure detected during execution runtime."
    exit 1
fi

# Step 3: Performance & Integrity Audit Logs
echo "Step 3: Compiling data storage delivery statistics..."
QUARANTINE_COUNT=$(ls -1 $QUARANTINE_DIR/quarantine_*.txt 2>/dev/null | wc -l)
PARQUET_COUNT=$(ls -1 $STAGING_DIR/staged_*.parquet 2>/dev/null | wc -l)

echo "======================================================================"
echo " PIPELINE EXECUTION AUDIT SUMMARY LOGS"
echo "======================================================================"
echo " Quarantined Error Files Generated : $QUARANTINE_COUNT"
echo " Staged Snappy Parquet Files Delivery: $PARQUET_COUNT"
echo "======================================================================"
echo " [SUCCESS] Unix Orchestration Wrapper completed operations safely."
echo "======================================================================"
