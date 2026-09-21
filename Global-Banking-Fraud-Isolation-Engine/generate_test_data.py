# ===================================================================================================
# FOLDER REPOSITORY : Global-Banking-Fraud-Isolation-Engine
# FILE NAME         : generate_test_data.py
# AUTHOR            : Sk Saiful Inam (Senior Data Lead)
# DESCRIPTION       : Generates the external raw transaction file for testing dynamic variables
# ===================================================================================================
import pandas as pd

payload = {
    "transaction_id": ["TXN101", "TXN102", "TXN103", "TXN103"],
    "account_number": ["ACC9001", "ACC9002", "ACC9003", "ACC9003"],
    "transaction_date": ["2026-09-09", "2026-09-11", "2026-09-11", "2026-09-11"],
    "transaction_amount": [5000.00, 125000.00, 450.00, 450.00],
    "fraud_risk_score": [0.12, 0.95, 0.05, 0.05],
    "last_updated": ["2026-09-09 09:00:00", "2026-09-11 10:15:00", "2026-09-11 11:30:00", "2026-09-11 11:45:00"]
}

df = pd.DataFrame(payload)
df.to_csv("daily_ledger.csv", index=False)
print(">>> SUCCESS: External 'daily_ledger.csv' file has been physically created on the server environment! <<<")
