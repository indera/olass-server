
-- Add the partners

INSERT INTO partner
    (partner_code, partner_description, partner_added_at)
VALUES
    ('UF',  'University of Florida', NOW()),
    ('HCN', 'Health Choice Network', NOW()),
    ('TMH', 'Tallahassee Memorial HealthCare', NOW()),
    ('OH',  'Orlando Health System', NOW()),
    ('FH',  'Florida Hospital', NOW()),
    ('MCH', 'Miami Children\'s Health System', NOW()),
    ('BOND', 'Bond Community Health Center Inc.', NOW())
;


-- Insert sample data
INSERT INTO linkage
    (partner_id, linkage_uuid, linkage_hash, linkage_added_at)
SELECT
    partner_id, bin_uuid(UUID()), lower(UNHEX(SHA2('first-last-dob-zip', 256))), NOW()
FROM
    partner
WHERE
    partner_code = 'UF'
;

INSERT INTO linkage
    (partner_id, linkage_uuid, linkage_hash, linkage_added_at)
SELECT
    partner_id, bin_uuid(UUID()), lower(UNHEX(SHA2('last-first-dob-zip', 256))), NOW()
FROM
    partner
WHERE
    partner_code = 'UF'
;

SELECT * FROM partner;

SELECT
    linkage_id, partner_code, lower(HEX(linkage_uuid)), lower(HEX(linkage_hash))
FROM
    linkage
    JOIN partner USING (partner_id)
WHERE
    linkage_hash = lower(UNHEX(SHA2('first-last-dob-zip', 256)));
