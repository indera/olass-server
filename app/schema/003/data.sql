
INSERT INTO oauth_user
    (email, added_at)
VALUES
    ('asura-root@ufl.edu', NOW()),
    ('asura-admin@ufl.edu', NOW()),
    ('asura-staff@ufl.edu', NOW())
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

SELECT * FROM oauth_user;
SELECT * FROM oauth_role;
SELECT * FROM oauth_user_role;
