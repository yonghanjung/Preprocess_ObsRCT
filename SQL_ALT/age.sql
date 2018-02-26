
DROP TABLE IF EXISTS age_yh;
CREATE TABLE age_yh AS
WITH agetbl AS
(
    SELECT ad.subject_id, ad.admittime,
    (extract(DAY FROM ad.admittime - p.dob)
            + extract(HOUR FROM ad.admittime - p.dob) / 24
            + extract(MINUTE FROM ad.admittime - p.dob) / 24 / 60
            ) / 365.25
            AS age
      FROM mimiciii.admissions ad
      INNER JOIN mimiciii.patients p
      ON ad.subject_id = p.subject_id
)
SELECT *
FROM agetbl