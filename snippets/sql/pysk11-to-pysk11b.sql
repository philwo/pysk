BEGIN;
ALTER TABLE "vps_virtualhost" ADD "enable_php" boolean;
ALTER TABLE "vps_virtualhost" ADD "owner_id" integer;
CREATE INDEX "vps_virtualhost_owner_id_idx" ON "vps_virtualhost" ("owner_id");

UPDATE "vps_virtualhost" SET "enable_php" = TRUE,
    "owner_id" = (SELECT id FROM app_customer ORDER BY id ASC LIMIT 1);

UPDATE vps_domain SET jabber = '' WHERE jabber IS NULL;    

UPDATE vps_mailbox SET quota = quota / 1024 WHERE quota > 1024;

COMMIT;

