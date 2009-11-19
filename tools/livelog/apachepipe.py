#!/usr/bin/env python
# -*- coding: utf-8 -*-

import apachelog, sys, MySQLdb
from optparse import OptionParser

def main(argv=None):
	if argv is None:
		argv = sys.argv

	parser = OptionParser()
	parser.add_option("-v", "--vhost", dest="vhostoverride", help="if logfile doesn't include vhost column, override it with this", metavar="VHOST")
	parser.add_option("-d", "--debug", action="store_true", dest="debug", help="Turn on debugging output", default=False)
	(options, args) = parser.parse_args(argv)

	debug = False

	if "-d" in argv[1:] or "--debug" in argv[1:]:
		debug = True

	if options.debug: print >> sys.stderr, "Debug mode activated"

	fallback = open("/var/log/apache2/fallback.log", "a")
	#fallback = open("/home/philwo/Coden/apachepipe/fallback.log", "a")

	try:
		db = MySQLdb.connect(host="db1.igowo.de", user="igowo_log_pipe", passwd="nw3nxWtfV9MfJA5w", db="igowo_log", charset="utf8", use_unicode=True)
		cursor = db.cursor()
	except MySQLdb.MySQLError:
		if options.debug: print >> sys.stderr, "Error: Could not connect to database"
		db = None
		cursor = None

	p_igowo = apachelog.parser(apachelog.formats["igowo"])
	p_vhextendedio = apachelog.parser(apachelog.formats["vhextendedio"])
	p_vhextended = apachelog.parser(apachelog.formats["vhextended"])
	p_extended = apachelog.parser(apachelog.formats["extended"])

	for line in sys.stdin:
		try:
			try:
				data = p_igowo.parse(line)
			except apachelog.ApacheLogParserError:
				try:
					data = p_vhextendedio.parse(line)
				except apachelog.ApacheLogParserError:
						try:
							data = p_vhextended.parse(line)
						except apachelog.ApacheLogParserError:
							if options.vhostoverride:
								data = p_extended.parse(line)
								data["%v"] = options.vhostoverride
							else:
								raise

			if cursor != None:
				vhost = data["%v"]

				if "%A" in data:
					local_ip = data["%A"]
				else:
					local_ip = ""

				if "%D" in data:
					utime = data["%D"]
				else:
					utime = None
				r_host = data["%h"]
				r_logname = data["%l"]
				r_user = data["%u"]
				datetime = apachelog.parse_date(data["%t"])

				request = data["%r"]
				status = int(data["%>s"])

				if data["%b"] != "-":
					response_size = int(data["%b"])
				else:
					response_size = 0

				referer = data["%{Referer}i"]
				user_agent = data["%{User-Agent}i"]

				if "%I" in data:
					bytes_recv = int(data["%I"])
				else:
					bytes_recv = None

				if "%O" in data:
					bytes_sent = int(data["%O"])
				else:
					bytes_sent = None

				query = "INSERT DELAYED INTO accesslog (vhost, local_ip, utime, r_host, r_logname, r_user, date, request, status, response_size, referer, user_agent, bytes_recv, bytes_sent) VALUES (%s, INET_ATON(%s), %s, INET_ATON(%s), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
				data = [vhost, local_ip, utime, r_host, r_logname, r_user, datetime, request, status, response_size, referer, user_agent, bytes_recv, bytes_sent]
				cursor.execute(query, data)
			else:
				fallback.write(line)
		except apachelog.ApacheLogParserError:
			if options.debug: print >> sys.stderr, "ApacheLogParserError on line %s" % line
			fallback.write(line)
			fallback.flush()
		except MySQLdb.MySQLError:
			if options.debug: print >> sys.stderr, "MySQLError on line %s" % line
			fallback.write(line)
			fallback.flush()
		except:
			sys.stderr.write("Unable to parse %s" % line)
			raise

if __name__ == "__main__":
	sys.exit(main())
