
DROP DATABASE IF EXISTS olass;
REVOKE ALL PRIVILEGES ON olass.* FROM 'olass'@'localhost';
DROP USER 'olass'@'localhost';
FLUSH PRIVILEGES;
