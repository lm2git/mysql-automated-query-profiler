-- Create the database and test tables
CREATE DATABASE IF NOT EXISTS testdb;

USE testdb;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50),
    email VARCHAR(100),
    age INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Populate the table with a large dataset
-- We generate 1,000,000 rows (you can adjust this number as needed)
DELIMITER $$
CREATE PROCEDURE PopulateLargeDataset()
BEGIN
    DECLARE i INT DEFAULT 1;
    WHILE i <= 1000 DO
        INSERT INTO users (name, email, age) 
        VALUES (
            CONCAT('User', i),
            CONCAT('user', i, '@example.com'),
            FLOOR(20 + (RAND() * 30))
        );
        SET i = i + 1;
    END WHILE;
END$$
DELIMITER ;

-- Call the procedure to insert rows
CALL PopulateLargeDataset();
