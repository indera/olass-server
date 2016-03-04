

CREATE DATABASE olass;

-- Create the user and grant privileges
CREATE USER 'olass'@'localhost' IDENTIFIED BY 'insecurepassword';

FLUSH PRIVILEGES;

GRANT
    ALL PRIVILEGES
ON
    olass.*
TO
    'olass'@'localhost';

USE olass;

CREATE DEFINER=`olass`@`localhost`
    FUNCTION `ordered_uuid`(uuid BINARY(36))
    RETURNS binary(16) DETERMINISTIC
    RETURN UNHEX(CONCAT(SUBSTR(uuid, 15, 4),SUBSTR(uuid, 10, 4),SUBSTR(uuid, 1, 8),SUBSTR(uuid, 20, 4),SUBSTR(uuid, 25)));
FLUSH PRIVILEGES;
