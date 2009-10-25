DROP VIEW IF EXISTS passwd_list;
DROP VIEW IF EXISTS server_ip_list;
DROP VIEW IF EXISTS server_ip_user_list;
DROP VIEW IF EXISTS pysk_vzlist;
ALTER TABLE vps_ipaddress DROP COLUMN server_id;
DROP TABLE IF EXISTS vps_server;

