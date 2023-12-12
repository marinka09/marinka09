DROP TABLE IF EXISTS "trigger_test";
CREATE TABLE "trigger_test"(
"trigger_testID" bigserial PRIMARY KEY,
"trigger_testName" text
);
DROP TABLE IF EXISTS "trigger_test_log";
CREATE TABLE "trigger_test_log"(
"id" bigserial PRIMARY KEY,
"trigger_test_log_ID" bigint,
"trigger_test_log_name" text
);

CREATE OR REPLACE FUNCTION after_insert_update_func() RETURNS TRIGGER as $trigger$
DECLARE
CURSOR_LOG CURSOR FOR SELECT * FROM "trigger_test_log";
row_ "trigger_test_log"%ROWTYPE;

BEGIN
IF old."trigger_testID" % 2 = 0 THEN
IF old."trigger_testID" % 3 = 0 THEN
RAISE NOTICE 'trigger_testID is multiple of 2 and 3';
FOR row_ IN CURSOR_LOG LOOP
UPDATE "trigger_test_log" SET "trigger_test_log_name" = '_' ||
row_."trigger_test_log_name" || '_log' WHERE "id" = row_."id";
END LOOP;
RETURN OLD;
ELSE
RAISE NOTICE 'trigger_testID is even';
INSERT INTO "trigger_test_log"("trigger_test_log_ID", "trigger_test_log_name")
VALUES (old."trigger_testID", old."trigger_testName");
UPDATE "trigger_test_log" SET "trigger_test_log_name" = trim(BOTH '_log' FROM
"trigger_test_log_name");
RETURN NEW;
END IF;
ELSE
RAISE NOTICE 'trigger_testID is odd';
FOR row_ IN CURSOR_LOG LOOP
UPDATE "trigger_test_log" SET "trigger_test_log_name" = '_' ||
row_."trigger_test_log_name" || '_log' WHERE "id" = row_."id";
END LOOP;
RETURN OLD;
END IF;
END;
$trigger$ LANGUAGE plpgsql;

CREATE TRIGGER "after_insert_update_trigger"
BEFORE DELETE OR UPDATE ON "trigger_test"
FOR EACH ROW

EXECUTE procedure after_insert_update_func();
INSERT INTO "trigger_test" ("trigger_testID", "trigger_testName")
SELECT
    generate_series(1, 3) * 3 AS "trigger_testID",
    'YourValueHere' AS "trigger_testName";
DELETE FROM "trigger_test_log";

UPDATE "trigger_test_log"
SET
  "trigger_test_log_name" = 'YourValueHere'
WHERE
  "id" % 2 = 0 AND
  "trigger_test_log_ID" % 2 = 0;
