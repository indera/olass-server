
-- Add users with the hashed password
INSERT INTO oauth_user
    (email, added_at, password_hash)
VALUES
    ('asura-root@ufl.edu', NOW(), '$6$rounds=666140$vQVDNQUwZCSDY0u7$kqmaQjQnYwWz9EQlms99UQDYaphVBwujnUs1H3XdhT741pY1HPirG1Y.oydcw3QtQnaMyVOspVZ20Dij7f24A/'),
    ('asura-admin@ufl.edu', NOW(), '$6$rounds=721306$o0JYbytB8UBzi.ap$ZJONXx83jYYi0atrdEloFJR7QK6j/5U3UJJv3t674.EeBRJ.Bu711lBGQZJA9hCaI.5MqUbiRHztj0moBCE3W0'),
    ('asura-staff@ufl.edu', NOW(), '$6$rounds=617908$4Flg0hww8CK5oDWU$FwGNlWtzTnl0WWrqNvAR/NLW9WNMQQgkM.dXgbFKhTGKZ1037Ev4BS/DxopiSMDw97PnlNDqDRLFL976qL4691')
;


INSERT INTO oauth_role
    (role_code, role_description)
VALUES
    ('root', 'the super-user can create admins'),
    ('admin', 'each partner can have admin members'),
    ('staff', 'each partner can have staff members')
;


INSERT INTO oauth_user_role (user_id, partner_id, role_id, added_at)
    SELECT
        u.id, p.partner_id, r.id, NOW()
    FROM
        oauth_user u, partner p, oauth_role r
    WHERE
        u.email = 'asura-root@ufl.edu'
        AND p.partner_code = 'UF'
        AND r.role_code = 'root'
UNION
    SELECT
        u.id, p.partner_id, r.id, NOW()
    FROM
        oauth_user u, partner p, oauth_role r
    WHERE
        u.email = 'asura-admin@ufl.edu'
        AND p.partner_code = 'UF'
        AND r.role_code = 'admin'
UNION
    SELECT
        u.id, p.partner_id, r.id, NOW()
    FROM
        oauth_user u, partner p, oauth_role r
    WHERE
        u.email = 'asura-staff@ufl.edu'
        AND p.partner_code = 'UF'
        AND r.role_code = 'staff'
;


INSERT INTO oauth_client
    (client_id, client_secret, user_id, _redirect_uris, _default_scopes, added_at)
SELECT
    'client_1', 'secret_1', u.id, '', '', NOW()
FROM
    oauth_user u
WHERE
    u.email = 'asura-root@ufl.edu'
;

-- Show sample data
SELECT * FROM oauth_user;
SELECT * FROM oauth_role;
SELECT * FROM oauth_user_role;

SELECT * FROM oauth_client;
