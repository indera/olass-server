
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

-- These rules have been extracted from 
INSERT INTO rule
    (rule_code, rule_description, rule_added_at)
VALUES
    ('F_L_D_Z',         'First Name + Last Name + DOB + Zip', NOW()),
    ('L_F_D_Z',         'Last Name + First Name + DOB + Zip', NOW()),
    ('F_L_D_C',         'First Name + Last Name + DOB + City', NOW()),
    ('L_F_D_C',         'Last Name + First Name + DOB + City', NOW()),
    ('3F_3L_SF_SL_D',   'Three Letter FN + Three Letter LN + Soundex FN + Soundex LN + DOB', NOW())
;

-- Insert sample data
INSERT INTO linkage
    (partner_id, rule_id, linkage_uuid, linkage_hash, linkage_added_at)
SELECT
    partner_id, rule_id, bin_uuid(UUID()), lower(UNHEX(SHA2('first-last-dob-zip', 256))), NOW()
FROM
    partner, rule
WHERE
    partner_code = 'UF'
    AND rule_code = 'F_L_D_Z'
;

INSERT INTO linkage
    (partner_id, rule_id, linkage_uuid, linkage_hash, linkage_added_at)
SELECT
    partner_id, rule_id, bin_uuid(UUID()), lower(UNHEX(SHA2('last-first-dob-zip', 256))), NOW()
FROM
    partner, rule
WHERE
    partner_code = 'UF'
    AND rule_code = 'L_F_D_Z'
;

SELECT * FROM partner;
SELECT * FROM rule;

SELECT
    linkage_id, partner_code, rule_code, lower(HEX(linkage_uuid)), lower(HEX(linkage_hash))
FROM
    linkage
    JOIN partner USING (partner_id)
    JOIN rule USING (rule_id)
WHERE
    linkage_hash = lower(UNHEX(SHA2('first-last-dob-zip', 256)));
