-- Create the telescope database if it doesn't exist
CREATE DATABASE IF NOT EXISTS telescope;

-- Create a user for the webportal project with full access
CREATE USER IF NOT EXISTS 'webportal'@'localhost' IDENTIFIED BY 'SEDSCelestia123';

-- Grant all privileges on the telescope database to the webportal user
GRANT ALL PRIVILEGES ON telescope.* TO 'webportal'@'localhost';

-- Apply the privileges
FLUSH PRIVILEGES;

-- Switch to the telescope database
USE telescope;

-- Create the webportal table for storing observation requests
CREATE TABLE IF NOT EXISTS webportal (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    exposure_time TIME,
    object VARCHAR(255),
    email VARCHAR(255),
    request_date DATE,
    request_time TIME,
    status ENUM('not captured', 'captured', 'mailed') DEFAULT 'not captured' NOT NULL,
    image_path VARCHAR(255) DEFAULT '/image'
);

-- Add an index on the email field for faster lookups
CREATE INDEX idx_email ON webportal(email);
