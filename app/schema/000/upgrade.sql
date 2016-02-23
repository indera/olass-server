

CREATE DATABASE olass;

-- Create the user and grant privileges
CREATE USER 'olass'@'localhost' IDENTIFIED BY 'insecurepassword';

FLUSH PRIVILEGES;

GRANT
    INSERT, SELECT, UPDATE, DELETE
    , SHOW VIEW
ON
    olass.*
TO
    'olass'@'localhost';

FLUSH PRIVILEGES;
