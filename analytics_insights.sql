-- ==============================================================================
-- PROJECT    : NSE-MarketData-Ingestion-Engine
-- COMPONENTS : Data Warehouse Analytical Query Worksheets & Quality Metrics
-- AUTHOR     : Sk Saiful Inam (Senior Data Lead)
-- ==============================================================================

--  INSIGHT 1: Extract High-Value Market Drivers using the Analytical View Layer
-- Purpose: Feeds business intelligence dashboards with high-performing tickers.
SELECT 
    ticker_symbol,
    trade_date,
    close_price,
    ingestion_timestamp
FROM 
    vw_high_value_tickers
LIMIT 10;


--  INSIGHT 2: Pipeline Data Quality & Operational Ingestion Audit Metrics
-- Purpose: Evaluates the health of the incoming Bhavcopy feeds for data governance teams.
SELECT 
    trade_date,
    COUNT(*) as total_rows_received,
    SUM(CASE WHEN clean_record_flag = 'Y' THEN 1 ELSE 0 END) as clean_rows_staged,
    SUM(CASE WHEN clean_record_flag = 'N' THEN 1 ELSE 0 END) as corrupt_rows_quarantined,
    ROUND(
        100.0 * SUM(CASE WHEN clean_record_flag = 'Y' THEN 1 ELSE 0 END) / COUNT(*), 
        2
    ) as data_quality_pass_percentage
FROM 
    nse_market_data_fact
GROUP BY 
    trade_date
ORDER BY 
    trade_date DESC;


--  INSIGHT 3: Market Breadth Analysis (Volume of Active Tickers)
-- Purpose: Tracks historical file ingestion processing volume over time.
SELECT 
    price_performance_tier,
    COUNT(DISTINCT ticker_symbol) as unique_ticker_count,
    ROUND(AVG(close_price), 2) as average_closing_price
FROM 
    nse_market_data_fact
GROUP BY 
    price_performance_tier;
