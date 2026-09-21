/* =================================================================================
   FILE NAME   : athena_audit_query.sql
   AUTHOR      : Sk Saiful Inam (Senior Data Lead)
   DESCRIPTION : Production audit query verifying schema integrity in Amazon Athena
   ================================================================================= */

SELECT 
    transaction_id, 
    account_number, 
    transaction_amount, 
    fraud_risk_score
FROM "target_banking_warehouse"."landing_zone"
WHERE fraud_risk_score > 0.90;
