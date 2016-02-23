
-- remove the tracking information
DELETE FROM version where version_id = '002';

DROP TABLE IF EXISTS linkage;
DROP TABLE IF EXISTS rule;
DROP TABLE IF EXISTS partner;
