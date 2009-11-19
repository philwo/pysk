--
-- PostgreSQL database dump
--

SET client_encoding = 'UTF8';
SET standard_conforming_strings = off;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET escape_string_warning = off;

REVOKE ALL ON DATABASE pysk FROM public;
GRANT ALL ON DATABASE pysk TO pysk;

REVOKE ALL ON SCHEMA public FROM public;
GRANT ALL ON SCHEMA public TO pysk;

--
-- Name: dovecot_passwd; Type: VIEW; Schema: public; Owner: pysk
--

CREATE VIEW dovecot_passwd AS
    SELECT (((m.mail)::text || '@'::text) || (d.name)::text) AS mail, m.password, ('user_quota=maildir:storage='::text || m.quota) AS quota, (((('/home/vmail/'::text || (d.name)::text) || '/'::text) || (m.mail)::text) || '/'::text) AS home FROM (vps_mailbox m JOIN vps_domain d ON ((m.domain_id = d.id))) WHERE (m.active = true);


ALTER TABLE public.dovecot_passwd OWNER TO pysk;

--
-- Name: postfix_virtual_domains; Type: VIEW; Schema: public; Owner: pysk
--

CREATE VIEW postfix_virtual_domains AS
    (SELECT DISTINCT d.name AS domain, 'dummy'::text AS target FROM (vps_mailbox m JOIN vps_domain d ON ((m.domain_id = d.id))) WHERE (m.active = true) ORDER BY d.name, 'dummy'::text) UNION (SELECT DISTINCT d.name AS domain, 'dummy'::text AS target FROM (vps_forwarding f JOIN vps_domain d ON ((f.domain_id = d.id))) WHERE (f.active = true) ORDER BY d.name, 'dummy'::text);


ALTER TABLE public.postfix_virtual_domains OWNER TO pysk;

--
-- Name: postfix_virtual_forwardings; Type: VIEW; Schema: public; Owner: pysk
--

CREATE VIEW postfix_virtual_forwardings AS
    (((SELECT (((f.source)::text || '@'::text) || (d.name)::text) AS source, f.target FROM (vps_forwarding f JOIN vps_domain d ON ((f.domain_id = d.id))) WHERE (f.active = true) UNION (SELECT DISTINCT ('postmaster@'::text || (d.name)::text) AS source, 'philipp@igowo.de'::text AS target FROM (vps_mailbox m JOIN vps_domain d ON ((m.domain_id = d.id))) ORDER BY ('postmaster@'::text || (d.name)::text), 'philipp@igowo.de'::text)) UNION (SELECT DISTINCT ('postmaster@'::text || (d.name)::text) AS source, 'philipp@igowo.de'::text AS target FROM (vps_forwarding f JOIN vps_domain d ON ((f.domain_id = d.id))) ORDER BY ('postmaster@'::text || (d.name)::text), 'philipp@igowo.de'::text)) UNION (SELECT DISTINCT ('abuse@'::text || (d.name)::text) AS source, 'philipp@igowo.de'::text AS target FROM (vps_mailbox m JOIN vps_domain d ON ((m.domain_id = d.id))) ORDER BY ('abuse@'::text || (d.name)::text), 'philipp@igowo.de'::text)) UNION (SELECT DISTINCT ('abuse@'::text || (d.name)::text) AS source, 'philipp@igowo.de'::text AS target FROM (vps_forwarding f JOIN vps_domain d ON ((f.domain_id = d.id))) ORDER BY ('abuse@'::text || (d.name)::text), 'philipp@igowo.de'::text);


ALTER TABLE public.postfix_virtual_forwardings OWNER TO pysk;

--
-- Name: postfix_virtual_mailboxes; Type: VIEW; Schema: public; Owner: pysk
--

CREATE VIEW postfix_virtual_mailboxes AS
    SELECT (((m.mail)::text || '@'::text) || (d.name)::text) AS mail, ((((d.name)::text || '/'::text) || (m.mail)::text) || '/Maildir/'::text) FROM (vps_mailbox m JOIN vps_domain d ON ((m.domain_id = d.id))) WHERE (m.active = true);


ALTER TABLE public.postfix_virtual_mailboxes OWNER TO pysk;

--
-- Name: stats_vhost_auth_list; Type: VIEW; Schema: public; Owner: pysk
--

CREATE VIEW stats_vhost_auth_list AS
    SELECT DISTINCT ltrim((((h.name)::text || '.'::text) || (d.name)::text), '.'::text) AS vhost, u.username, md5((((u.username)::text || ':stats:'::text) || (c.statspw)::text)) AS digest FROM vps_virtualhost h, vps_domain d, auth_user u, app_customer c WHERE ((((h.domain_id = d.id) AND (h.owner_id = u.id)) AND (u.id = c.user_id)) AND ((c.statspw)::text <> ''::text)) ORDER BY ltrim((((h.name)::text || '.'::text) || (d.name)::text), '.'::text), u.username, md5((((u.username)::text || ':stats:'::text) || (c.statspw)::text));


ALTER TABLE public.stats_vhost_auth_list OWNER TO pysk;

