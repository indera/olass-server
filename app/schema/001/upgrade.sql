
-- Store database modification log
CREATE TABLE version (
   version_id varchar(255) NOT NULL DEFAULT '',
   version_stamp timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
   version_info text NOT NULL,
  PRIMARY KEY (version_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO version (version_id, version_stamp, version_info)
   VALUES('001', now(), 'New table: version')
;


SHOW TABLES;
SELECT * FROM version;
