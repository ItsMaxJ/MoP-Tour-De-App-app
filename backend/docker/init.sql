-- init.sql
CREATE DATABASE IF NOT EXISTS product;
CREATE USER IF NOT EXISTS 'tda_user'@'%' IDENTIFIED BY 'strongPassword?';
GRANT ALL PRIVILEGES ON product.* TO 'tda_user'@'%';
FLUSH PRIVILEGES;