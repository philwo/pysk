# Pysk - Python Server Konfigurator
by Philipp Wollermann

## History
Pysk was developed over the course of five years (2006 -  2011) by me, because I needed a software to manage my server infrastructure for my web hosting business (igowo). It was meant to be open-sourced quickly, but lots of hardcoded customer data and passwords, licensing issues, ugly source, lack of time, … kept me from actually publishing it. Finally, in 2012, I converted the trusty old hg repository to Git, rewrote history to remove the customer data and third-party components. Now, most of that is fixed. If you look hard, you can still find some hardcoded passwords in the history of some files, but I'd suggest you don't bother, because the whole infrastructure from those days was shut down over a year ago, and all data deleted, so they can't be used anywhere. I could easily remove those parts, but then I'd have to change the history of the repository even more and you couldn't learn from looking at how the scripts really worked together and were developed.

## Current state
I didn't touch anything for over a year, but it was once a fully working system in daily use, managing over 40 virtual servers. There was a branch in which I heavily refactored everything, but it was non-functional at that time and was unfortunately lost. If you dig around, you'll find lots of interesting stuff, which is partly documented below - feel free to build your own management software using parts of Pysk. (Though you should probably have a look at Puppet or Chef before reinventing the wheel once again.)

## Architecture
Pysk is installed on the hypervisor and on every virtual machine. Not all of Pysk's functionality is needed on every machine - for example, the hypervisor doesn't have a web interface yet, so the Django-based app isn't used.

### doc/
Contains some personal notes for upgrading between versions, etc.

### etc/serverconfig/
Contains configuration switches and allows overriding them for individual servers.

- etc/serverconfig/default: Default configuration switches
- etc/serverconfig/<hostname>: Create a file with the name of the server whose switches you want to override (see mikuru.igowo.de)
- etc/serverconfig/exclude/<hostname>: Create a file with the name of the server, then list files which shouldn't be overwritten by the configuration management run (see kyon.igowo.de)

### pysk/
This is the Django-based management app, which contains the data models and admin interface to administer the virtual server.

#### pysk/templates/
This contains the tree of configuration files that is generated using the Django template syntax.

### secret/
Contains secret files individual to every managed virtual server and gets automatically filled on the first run.

### serverconfig/
This contains the tree of configuration files that is rsync'd as-is or only marginally modified using shell scripts. (This is a bit ugly and was thus removed in the lost branch and merged into pysk/templates/)

### snippets/
Contains small helper scripts which became necessary to do system migrations on managed virtual servers.

### static/
Some small helper files used by the admin interface (CSS stylesheets, JavaScript libraries, …)

### tools/
Lots of Pysk's functionality is provided in form of helper scripts, to be used by the admin whenever necessary or called automatically by the configuration management run.

#### tools/backup/
System backup using duplicity.

#### tools/dns/
This is a program for the automatic generation of a centralized DNS server config, including the zones of all served domains, by fetching all needed records from the virtual servers via the HTTP API and merging them semi-intelligently. The serial number is incremented automatically as needed, whenever the hash sum of a zone file changes.

#### tools/hypervisor/
Contains scripts used for bootstrapping new Arch Linux and Debian servers and for managing them centrally.

#### tools/logfiles/
Parsing the logfiles of webservers and using them to analyze traffic on one's website is bad enough. Most web hosters don't care to generate valid statistics, because the users don't care, as long as the shiny numbers keep increasing. I delayed the delivery of this feature to my customers over and over, because it's so hard to get right. This software was made to finally solve this darn task once and for all (hint: it was better than the alternatives, but still didn't). It collects webserver logfiles from the local disk or an IMAP postbox, merges them, removes corrupted lines, builds a DNS cache file for AWstats using very fast multi-threaded resolving and just puts everything together so everything works, as the user expects it.

Seriously, just use Google Analytics or Piwik instead of bothering with your webservers' logfiles.

#### tools/mysql/ and tools/postgres/
Some helper scripts to maintain MySQL and PostgreSQL databases.

#### tools/passwd/
Scripts for syncing the Django user database to /etc/passwd, /etc/group and /etc/shadow. If you add a user in Django, he'll be able to login via SSH. If you edit his password in Django, it will be changed for the unix user too.

Note: It would be even more awesome to write an NSS and PAM module to query the Django database.

#### tools/ssl/
Some scripts for generating CSRs and implementing SSL on the server.

#### vendors/
Contained a local copy of Django and django_extensions, because at that time I didn't know about virtualenv. Now I'd just use a requirements.txt and virtualenv.

#### www/
Contained phpMyAdmin, phpPgAdmin, phpSysInfo, Roundcube Webmail and BetterAWstats when it was in use at igowo. Now it's empty, so you have to fill it yourself. You can find the configs I used in the doc/ directory.

#### wwwlogs/
Contained the webserver logs processed by tools/logfiles. Don't ask me, why they were stored inside the source tree. ;)

## Have fun with Pysk!
