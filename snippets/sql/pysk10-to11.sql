BEGIN;
-- Steps for migration
-- 
-- 1) SSL hosts must be dealed manually with
-- 2) Check that every virtualhost only has one HostConfig
-- 3) Delete 127.0.0.1 ipaddress, make sure every HostConfig uses the public IP

-- Drop obsolete views
DROP VIEW "dovecot_passwd";
DROP VIEW "passwd_list_all";
DROP VIEW "postfix_virtual_domains";
DROP VIEW "postfix_virtual_forwardings";
DROP VIEW "postfix_virtual_mailboxes";
DROP VIEW "stats_vhost_auth_list";

-- Drop "owner_id" of all models
ALTER TABLE "vps_domain"      DROP COLUMN "owner_id";
ALTER TABLE "vps_virtualhost" DROP COLUMN "owner_id";
ALTER TABLE "vps_alias"	      DROP COLUMN "owner_id";
ALTER TABLE "vps_mailbox"     DROP COLUMN "owner_id";
ALTER TABLE "vps_forwarding"  DROP COLUMN "owner_id";

-- Model: Alias
ALTER TABLE "vps_alias"       DROP COLUMN "wildcard";

-- Model: DirectAlias
ALTER TABLE "vps_directalias" DROP COLUMN "ipport_id";
ALTER TABLE "vps_directalias" ALTER "name" TYPE varchar(255);

-- Model: VirtualHost
ALTER TABLE "vps_virtualhost" ADD "ipport_id" integer;
ALTER TABLE "vps_virtualhost" ADD "force_www" varchar(16);
ALTER TABLE "vps_virtualhost" ADD "ssl_enabled" boolean;
ALTER TABLE "vps_virtualhost" ADD "ssl_force" boolean;
ALTER TABLE "vps_virtualhost" ADD "ssl_cert" varchar(250);
ALTER TABLE "vps_virtualhost" ADD "ssl_key" varchar(250);
ALTER TABLE "vps_virtualhost" ADD "apache_config" text;
ALTER TABLE "vps_virtualhost" ADD "apache_enabled" boolean;
ALTER TABLE "vps_virtualhost" ADD "nginx_config" text;

UPDATE "vps_virtualhost" SET nginx_config = '';

CREATE INDEX "vps_virtualhost_ipport_id_idx"
	ON "vps_virtualhost" ("ipport_id");

UPDATE "vps_virtualhost" SET
    "ipport_id" = "vps_hostconfig"."ipport_id",
    "force_www" = 'ignore',
    "ssl_enabled" = FALSE,
    "ssl_force" = FALSE,
    "ssl_cert" = "vps_ipaddress"."sslcert",
    "ssl_key" = "vps_ipaddress"."sslkey",
    "apache_config" = "vps_hostconfig"."config",
    "apache_enabled" = TRUE
    FROM vps_ipaddress, vps_hostconfig
    WHERE "vps_virtualhost"."id" = "vps_hostconfig"."host_id"
    AND "vps_hostconfig"."ipport_id" = "vps_ipaddress"."id";

-- Model: IPAddress
ALTER TABLE "vps_ipaddress" DROP COLUMN "port";
ALTER TABLE "vps_ipaddress" DROP COLUMN "sslcert";
ALTER TABLE "vps_ipaddress" DROP COLUMN "sslca";
ALTER TABLE "vps_ipaddress" DROP COLUMN "sslkey";
ALTER TABLE "vps_ipaddress" DROP COLUMN "configtype";
ALTER TABLE "vps_ipaddress" DROP COLUMN "parent_ip_id";
ALTER TABLE "vps_ipaddress" ADD UNIQUE ("ip");

-- Model: Domain
ALTER TABLE "vps_domain"    ADD "jabber" varchar(255);

-- Application: vps
DROP TABLE "vps_hostconfig";

-- Clean old crap.
DROP TABLE IF EXISTS voip_cdr;
DROP TABLE IF EXISTS voip_destination;
DROP TABLE IF EXISTS voip_sipaccount;

DELETE FROM auth_permission USING django_content_type WHERE auth_permission.content_type_id = django_content_type.id AND django_content_type.app_label = 'voip';
DELETE FROM django_content_type WHERE app_label = 'voip';

COMMIT;
