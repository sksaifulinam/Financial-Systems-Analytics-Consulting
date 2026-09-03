-- ==============================================================================
-- PROJECT    : NSE-MarketData-Ingestion-Engine
-- COMPONENTS : AWS Redshift / PostgreSQL Target Warehouse Storage Layer DDL
-- AUTHOR     : Sk Saiful Inam (Senior Data Lead)
-- ==============================================================================

-- 1. Create the Production Fact Target Table for Staging Clean Data
CREATE TABLE IF NOT EXISTS nse_market_data_fact (
    ticker_symbol         VARCHAR(20) NOT NULL,
    trade_date            DATE NOT NULL,
    close_price           NUMERIC(12, 4) NOT NULL,
    account_status        VARCHAR(30),
    ingestion_timestamp   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    clean_record_flag     CHAR(1) DEFAULT 'Y',
    price_performance_tier VARCHAR(30),
    
    -- Target Warehouse constraints for performance tracking
    PRIMARY KEY (ticker_symbol, trade_date)
);

-- COMMENT blocks to maintain enterprise data dictionary standards
COMMENT ON TABLE nse_market_data_fact IS 'Fact table housing clean, enriched daily National Stock Exchange ingestion feeds.';

-- 2. Create an Optimized View for Downstream Business Intelligence Analytics
CREATE OR REPLACE VIEW vw_high_value_tickers AS
SELECT 
    ticker_symbol,
    trade_date,
    close_price,
    ingestion_timestamp
FROM 
    nse_market_data_fact
WHERE 
    price_performance_tier = 'High Value'
ORDER BY 
    close_price DESC;
