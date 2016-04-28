
-- add oauth tables

CREATE TABLE oauth_user (
    id int(11) NOT NULL AUTO_INCREMENT,
    email varchar(255) NOT NULL,
    first_name varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL,
    last_name varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL,
    mi_name char(1) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL,
    password_hash varchar(255) DEFAULT NULL,
    added_at datetime DEFAULT NULL,
 PRIMARY KEY (id),
 UNIQUE KEY email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
;

CREATE TABLE oauth_client (
    id varchar(40) NOT NULL,
    client_secret varchar(55) NOT NULL,
    user_id int(11) NOT NULL,
    _redirect_uris text,
    _default_scopes text,
    added_at datetime DEFAULT NULL,
 PRIMARY KEY (id),
 KEY user_id (user_id),
 CONSTRAINT `fk_client_user_id` FOREIGN KEY (user_id) REFERENCES oauth_user (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
;

-- A grant token is created in the authorization flow, and will be destroyed when the authorization finished.
-- Ideally we would store grant_tokens in a cache (such as redis) for better performance
CREATE TABLE oauth_grant_token (
    id int(11) NOT NULL AUTO_INCREMENT,
    client_id varchar(40) NOT NULL,
    code varchar(255) NOT NULL,
    redirect_uri varchar(255) DEFAULT NULL,
    expires datetime DEFAULT NULL,
    _scopes text,
    added_at datetime DEFAULT NULL,
 PRIMARY KEY (id),
 KEY (client_id),
 KEY (code),
 CONSTRAINT `fk_grant_client_id` FOREIGN KEY (client_id) REFERENCES oauth_client (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8
;

CREATE TABLE oauth_client_token (
    id int(11) NOT NULL AUTO_INCREMENT,
    client_id varchar(40) NOT NULL,
    token_type varchar(40) DEFAULT NULL,
    access_token varchar(255) DEFAULT NULL,
    refresh_token varchar(255) DEFAULT NULL,
    expires datetime DEFAULT NULL,
    _scopes text,
    added_at datetime DEFAULT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY (access_token),
  UNIQUE KEY (refresh_token),
  KEY (client_id),
  CONSTRAINT `fk_client_client_id` FOREIGN KEY (client_id) REFERENCES oauth_client (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8
;
