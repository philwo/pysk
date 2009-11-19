#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading, Queue, socket, sys, MySQLdb

class ResolveThread(threading.Thread):
	def __init__(self, inputQueue, outputDict):
		threading.Thread.__init__(self)
		self.inputQueue = inputQueue
		self.outputDict = outputDict
		self.db = MySQLdb.connect(host="db1.igowo.de", user="igowo_log_rdns", passwd="4EqKYjbMmMVfPWct", db="igowo_log", charset="utf8", use_unicode=True)
		self.cursor = self.db.cursor()

	def run(self):
		try:
			while True:
				i = self.inputQueue.get_nowait()

				try:
					rdns = socket.gethostbyaddr(i)[0]
				except socket.herror:
					# If we can't resolve it, store the IP
					rdns = i

				#print "%s = %s" % (i, rdns)
				self.outputDict[i] = rdns
		except Queue.Empty:
			pass

def main(argv=None):
	if argv is None:
		argv = sys.argv

	db = MySQLdb.connect(host="db1.igowo.de", user="igowo_log_rdns", passwd="4EqKYjbMmMVfPWct", db="igowo_log", charset="utf8", use_unicode=True)
	cursor = db.cursor()
	cursor.execute("SELECT DISTINCT INET_NTOA(r_host) FROM accesslog WHERE rdns IS NULL")
	rows = cursor.fetchall()

	inputQueue = Queue.Queue()
	for row in rows:
		inputQueue.put(row[0])

	outputDict = {}
	workers = [ResolveThread(inputQueue, outputDict) for i in range(0, 100)]
	for worker in workers:
		worker.start()
	for worker in workers:
		worker.join()

	#print "Updating database ..."
	for ip, rdns in outputDict.iteritems():
		query = "UPDATE accesslog SET rdns = %s WHERE rdns IS NULL AND r_host = INET_ATON(%s)"
		data = [rdns, ip]
		cursor.execute(query, data)

if __name__ == "__main__":
	sys.exit(main())
