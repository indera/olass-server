
-- add oauth tables

CREATE TABLE user (
    id int(11) NOT NULL AUTO_INCREMENT,
    email varchar(255) NOT NULL,
    first_name varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
    last_name varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
    mi_name char(1) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
    password_hash varchar(255) NOT NULL DEFAULT '',
    added_at datetime DEFAULT NULL,
 PRIMARY KEY (id),
 UNIQUE KEY email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
;

CREATE TABLE client (
    id varchar(40) NOT NULL,
    client_secret varchar(55) NOT NULL,
    user_id int(11) DEFAULT NULL,
    _redirect_uris text,
    _default_scopes text,
    added_at datetime DEFAULT NULL,
 PRIMARY KEY (id),
 KEY user_id (user_id),
 CONSTRAINT `fk_client_user_id` FOREIGN KEY (user_id) REFERENCES `user` (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
;

CREATE TABLE `grant` (
    id int(11) NOT NULL AUTO_INCREMENT,
    user_id int(11) DEFAULT NULL,
    client_id varchar(40) NOT NULL,
    code varchar(255) NOT NULL,
    redirect_uri varchar(255) DEFAULT NULL,
    expires datetime DEFAULT NULL,
    _scopes text,
    added_at datetime DEFAULT NULL,
 PRIMARY KEY (id),
 KEY (user_id),
 KEY (client_id),
 KEY (code),
 CONSTRAINT `fk_grant_user_id` FOREIGN KEY (user_id) REFERENCES `user` (id) ON DELETE CASCADE,
 CONSTRAINT `fk_grant_client_id` FOREIGN KEY (client_id) REFERENCES client (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
;

CREATE TABLE token (
    id int(11) NOT NULL AUTO_INCREMENT,
    client_id varchar(40) NOT NULL,
    user_id int(11) DEFAULT NULL,
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
  KEY (user_id),
  CONSTRAINT `fk_token_client_id` FOREIGN KEY (client_id) REFERENCES client (id),
  CONSTRAINT `fk_token_user_id` FOREIGN KEY (user_id) REFERENCES `user` (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
;
