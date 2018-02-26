-- --------------------------------------------------------
-- Title: Create a distribution of BUN values for adult hospital admissions
-- Notes: this query does not specify a schema. To run it on your local
-- MIMIC schema, run the following command:
--  SET SEARCH_PATH TO mimiciii;
-- Where "mimiciii" is the name of your schema, and may be different.
-- --------------------------------------------------------

DROP TABLE IF EXISTS bun_tbl;
CREATE TABLE bun_tbl AS
WITH agetbl AS
(
    SELECT ad.subject_id
    FROM mimiciii.admissions ad
    INNER JOIN mimiciii.patients p
    ON ad.subject_id = p.subject_id
    WHERE
     -- filter to only adults
    EXTRACT(EPOCH FROM (ad.admittime - p.dob))/60.0/60.0/24.0/365.242 > 15
    -- group by subject_id to ensure there is only 1 subject_id per row
    group by ad.subject_id
)
, bun as
(
  SELECT width_bucket(valuenum, 0, 280, 280) AS bucket
  FROM mimiciii.labevents le
  INNER JOIN agetbl
  ON le.subject_id = agetbl.subject_id
  WHERE itemid IN (51006)
)
SELECT bucket as blood_urea_nitrogen, count(*)
FROM bun
GROUP BY bucket
ORDER BY bucket;