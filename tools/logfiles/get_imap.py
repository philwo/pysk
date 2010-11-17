#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import with_statement

import sys, os, os.path
from imaplib import IMAP4
from email import message_from_string
from tempfile import mkstemp

def main(argv=None):
    M = IMAP4("imap.igowo.de")
    M.login("webstats@intra.igowo.de", "c9Pf6G6vAAV3")
    M.select()
    typ, data = M.sort("DATE", "UTF-8", "UNSEEN")

    OUTPUTDIR = "/opt/pysk/wwwlogs"

    for num in data[0].split():
        typ, data = M.fetch(num, "(BODY.PEEK[])")
        msg = message_from_string(data[0][1])

        if msg["Subject"].find("access.log") != -1:
            (output_handle, output_name) = mkstemp(dir=os.path.join(OUTPUTDIR, "inbox"))
            with os.fdopen(output_handle, "w+b") as output_file:
                for part in msg.walk():
                    if part.get_content_type() != "text/plain":
                        continue
                    output_file.writelines(part.get_payload(decode=True))
                    M.store(num, "+FLAGS", r"\Seen")
    M.close()
    M.logout()

if __name__ == "__main__":
    sys.exit(main())
