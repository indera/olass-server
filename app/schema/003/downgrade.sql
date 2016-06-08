
-- remove the tracking information
DELETE FROM version where version_id = '003';

-- remove oauth tables
DROP TABLE oauth_access_token;
DROP TABLE oauth_client;
DROP TABLE oauth_user_role;
DROP TABLE oauth_role;
DROP TABLE oauth_user;
