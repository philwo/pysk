BEGIN;
-- Application: vps
-- Model: VirtualHost
ALTER TABLE "vps_virtualhost"
    ADD "php_config_id" integer;
CREATE INDEX "vps_virtualhost_php_config_id_idx"
    ON "vps_virtualhost" ("php_config_id");
-- Model: PHPConfig
-- Table missing: vps_phpconfig
-- Model: PHPExtension
-- Table missing: vps_phpextension
-- Model: ServerConfig
-- Table missing: vps_serverconfig
COMMIT;


