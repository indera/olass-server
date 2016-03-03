
-- Add the partners

INSERT INTO partner
    (partner_code, partner_description, partner_added_at)
VALUES
    ('UF',  'University of Florida', NOW()),
    ('HCN', 'Health Choice Network', NOW()),
    ('TMH', 'Tallahase Memorial HealthCare', NOW()),
    ('OH',  'Orlando Health System', NOW()),
    ('FH',  'Florida Hospital', NOW()),
    ('MCH', 'Miami Children\'s Health System', NOW()),
    ('BOND', 'Bond Community Health Center Inc.', NOW())
;

-- These rules have been extracted from 
INSERT INTO rule
    (rule_code, rule_description, rule_added_at)
VALUES
    ('F-L-D-Z',         'First Name + Last Name + DOB + Zip', NOW()),
    ('L-F-D-Z',         'Last Name + First Name + DOB + Zip', NOW()),
    ('F-L-D-C',         'First Name + Last Name + DOB + City', NOW()),
    ('L-F-D-C',         'Last Name + First Name + DOB + City', NOW()),
    ('3F-3L-SF-SL-D',   'Three Letter FN + Three Letter LN + Soundex FN + Soundex LN + DOB', NOW())
;

-- Insert sample data
INSERT INTO linkage
    (partner_id, rule_id, linkage_uuid, linkage_hash, linkage_added_at)
SELECT
    partner_id, rule_id, UUID(), SHA2('First-Last-DOB-Zip', 256), NOW()
FROM
    partner, rule
WHERE
    partner_code = 'UF'
    AND rule_code = 'F-L-D-Z'
;

INSERT INTO linkage
    (partner_id, rule_id, linkage_uuid, linkage_hash, linkage_added_at)
SELECT
    partner_id, rule_id, UUID(), SHA2('Last-First-DOB-Zip', 256), NOW()
FROM
    partner, rule
WHERE
    partner_code = 'UF'
    AND rule_code = 'L-F-D-Z'
;
