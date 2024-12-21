CREATE DATABASE shipping_benchmark;

CREATE TABLE market_rates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE NOT NULL,
    origin VARCHAR(255) NOT NULL,
    destination VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL
);

CREATE TABLE aggregated_market_rates (
    date DATE NOT NULL,
    origin VARCHAR(255) NOT NULL,
    destination VARCHAR(255) NOT NULL,
    min_price DECIMAL(10, 2),
    percentile_10_price DECIMAL(10, 2),
    median_price DECIMAL(10, 2),
    percentile_90_price DECIMAL(10, 2),
    max_price DECIMAL(10, 2)
);
ALTER TABLE aggregated_market_rates ADD UNIQUE KEY (date, origin, destination);

CREATE TABLE users_rates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_email VARCHAR(255) NOT NULL,
    origin VARCHAR(255) NOT NULL,
    destination VARCHAR(255) NOT NULL,
    effective_date DATE NOT NULL,
    expiry_date DATE NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    annual_volume DECIMAL(10, 2) NOT NULL
);


-- Create a scheduled query to insert the aggregated data from market_rates to aggregated_market_rates
DELIMITER $$
CREATE EVENT sync_aggregated_market_rates
ON SCHEDULE EVERY 10 MINUTE
DO
BEGIN
    INSERT INTO aggregated_market_rates (
        date, origin, destination, min_price, percentile_10_price, median_price, percentile_90_price, max_price
    )
    SELECT
        date,
        origin,
        destination,
        MIN(price) AS min_price,
        MAX(CASE WHEN ROW_NUMBER() OVER (PARTITION BY date, origin, destination ORDER BY price ASC) = FLOOR(0.1 * (COUNT(*) OVER (PARTITION BY date, origin, destination) - 1)) + 1 THEN price END) AS percentile_10_price,
        MAX(CASE WHEN ROW_NUMBER() OVER (PARTITION BY date, origin, destination ORDER BY price ASC) = FLOOR(0.5 * (COUNT(*) OVER (PARTITION BY date, origin, destination) - 1)) + 1 THEN price END) AS median_price,
        MAX(CASE WHEN ROW_NUMBER() OVER (PARTITION BY date, origin, destination ORDER BY price ASC) = FLOOR(0.9 * (COUNT(*) OVER (PARTITION BY date, origin, destination) - 1)) + 1 THEN price END) AS percentile_90_price,
        MAX(price) AS max_price
    FROM
        market_rates
    GROUP BY
        date, origin, destination
    ON DUPLICATE KEY UPDATE
        min_price = VALUES(min_price),
        percentile_10_price = VALUES(percentile_10_price),
        median_price = VALUES(median_price),
        percentile_90_price = VALUES(percentile_90_price),
        max_price = VALUES(max_price);
END $$
DELIMITER ;

