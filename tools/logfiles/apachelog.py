#!/usr/bin/env python2
# -*- coding: utf-8 -*-

__version__ = "1.1-igowo"
__license__ = """Released under the same terms as Perl.
See: http://dev.perl.org/licenses/
"""
__author__ = "Harry Fuecks <hfuecks@gmail.com>"
__contributors__ = [
    "Peter Hickman <peterhi@ntlworld.com>",
    "Loic Dachary <loic@dachary.org>",
    "Philipp Wollermann <philipp.wollermann@gmail.com>"
    ]

import re
from datetime import datetime, timedelta


class ApacheLogParserError(Exception):
    pass


class parser:
    def __init__(self, format):
        """
        Takes the log format from an Apache configuration file.

        Best just copy and paste directly from the .conf file
        and pass using a Python raw string e.g.

        format = r'%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"'
        p = apachelog.parser(format)
        """
        self._names = []
        self._regex = None
        self._pattern = ''
        self._parse_format(format)

    def _parse_format(self, format):
        """
        Converts the input format to a regular
        expression, as well as extracting fields

        Raises an exception if it couldn't compile
        the generated regex.
        """
        format = format.strip()
        format = re.sub('[ \t]+', ' ', format)

        subpatterns = []

        findquotes = re.compile(r'^\\"')
        findreferreragent = re.compile('Referer|User-Agent', re.I)
        findpercent = re.compile('^%.*t$')
        lstripquotes = re.compile(r'^\\"')
        rstripquotes = re.compile(r'\\"$')
        self._names = []

        for element in format.split(' '):

            hasquotes = 0
            if findquotes.search(element):
                hasquotes = 1

            if hasquotes:
                element = lstripquotes.sub('', element)
                element = rstripquotes.sub('', element)

            self._names.append(self.alias(element))

            subpattern = '(\S*)'

            if hasquotes:
                if element == '%r' or findreferreragent.search(element):
                    subpattern = r'\"([^"\\]*(?:\\.[^"\\]*)*)\"'
                else:
                    subpattern = r'\"([^\"]*)\"'

            elif findpercent.search(element):
                subpattern = r'(\[[^\]]+\])'

            elif element == '%U':
                subpattern = '(.+?)'

            subpatterns.append(subpattern)

        self._pattern = '^' + ' '.join(subpatterns) + '$'
        try:
            self._regex = re.compile(self._pattern)
        except Exception, e:
            raise ApacheLogParserError(e)

    def parse(self, line):
        """
        Parses a single line from the log file and returns
        a dictionary of it's contents.

        Raises and exception if it couldn't parse the line
        """
        line = line.strip()
        match = self._regex.match(line)

        if match:
            data = {}
            for k, v in zip(self._names, match.groups()):
                data[k] = v
            return data

        raise ApacheLogParserError("Unable to parse: %s with the %s regular expression" % (line, self._pattern))

    def alias(self, name):
        """
        Override / replace this method if you want to map format
        field names to something else. This method is called
        when the parser is constructed, not when actually parsing
        a log file

        Takes and returns a string fieldname
        """
        return name

    def pattern(self):
        """
        Returns the compound regular expression the parser extracted
        from the input format (a string)
        """
        return self._pattern

    def names(self):
        """
        Returns the field names the parser extracted from the
        input format (a list)
        """
        return self._names

months = {
    'Jan': 1,
    'Feb': 2,
    'Mar': 3,
    'Apr': 4,
    'May': 5,
    'Jun': 6,
    'Jul': 7,
    'Aug': 8,
    'Sep': 9,
    'Oct': 10,
    'Nov': 11,
    'Dec': 12
}


def parse_date(date):
    """
    Takes a date in the format: [05/Dec/2006:10:51:44 +0000]
    (including square brackets) and returns a DateTime object
    in UTC time.
    """

    # Strip off the brackets
    date = date[1:-1]

    year = int(date[7:11])
    month = months[date[3:6]]
    day = int(date[0:2])
    hour = int(date[12:14])
    minute = int(date[15:17])
    second = int(date[18:20])

    tzop = date[21]
    tzhour = int(date[22:24])
    tzmin = int(date[24:26])
    tzdelta = timedelta(hours=tzhour, minutes=tzmin)

    dt = datetime(year, month, day, hour, minute, second)

    if tzop == "+":
        dt -= tzdelta
    elif tzop == "-":
        dt += tzdelta
    else:
        raise Exception("Invalid date string, timezone op is neither + nor -!")

    return dt

"""
Frequenty used log formats stored here
"""
formats = {
    # Common Log Format (CLF)
    'common': r'%h %l %u %t \"%r\" %>s %b',

    # Common Log Format with Virtual Host
    'vhcommon': r'%v %h %l %u %t \"%r\" %>s %b',

    # igowo logformats
    # igowo = LocalIP ServeTimeMikroSecs VirtualHost RemoteHost - RequestDateTime FirstLineOfRequest StatusCode BodySizeBytes Referer User-Agent InputBytes OutputBytes
    'igowo':        r'%A %D %v %h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\" %I %O',
    'vhextendedio': r'%v %h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\" %I %O',
    'vhextended':   r'%v %h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"',
    'extended':     r'%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"',
    }

if __name__ == '__main__':
    import unittest

    class TestApacheLogParser(unittest.TestCase):

        def setUp(self):
            self.format = r'%h %l %u %t \"%r\" %>s '\
                        r'%b \"%{Referer}i\" \"%{User-Agent}i\"'
            self.fields = '%h %l %u %t %r %>s %b %{Referer}i '\
                        '%{User-Agent}i'.split(' ')
            self.pattern = '^(\\S*) (\\S*) (\\S*) (\\[[^\\]]+\\]) '\
                        '\\\"([^"\\\\]*(?:\\\\.[^"\\\\]*)*)\\\" '\
                        '(\\S*) (\\S*) \\\"([^"\\\\]*(?:\\\\.[^"\\\\]*)*)\\\" '\
                        '\\\"([^"\\\\]*(?:\\\\.[^"\\\\]*)*)\\\"$'
            self.line1 = r'212.74.15.68 - - [23/Jan/2004:11:36:20 +0000] '\
                        r'"GET /images/previous.png HTTP/1.1" 200 2607 '\
                        r'"http://peterhi.dyndns.org/bandwidth/index.html" '\
                        r'"Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.2) '\
                        r'Gecko/20021202"'
            self.line2 = r'212.74.15.68 - - [23/Jan/2004:11:36:20 +0000] '\
                        r'"GET /images/previous.png=\" HTTP/1.1" 200 2607 '\
                        r'"http://peterhi.dyndns.org/bandwidth/index.html" '\
                        r'"Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.2) '\
                        r'Gecko/20021202"'
            self.line3 = r'4.224.234.46 - - [20/Jul/2004:13:18:55 -0700] '\
                        r'"GET /core/listing/pl_boat_detail.jsp?&units=Feet&checked'\
                        r'_boats=1176818&slim=broker&&hosturl=giffordmarine&&ywo='\
                        r'giffordmarine& HTTP/1.1" 200 2888 "http://search.yahoo.com/'\
                        r'bin/search?p=\"grady%20white%20306%20bimini\"" '\
                        r'"Mozilla/4.0 (compatible; MSIE 6.0; Windows 98; '\
                        r'YPC 3.0.3; yplus 4.0.00d)"'
            self.p = parser(self.format)

        def testpattern(self):
            self.assertEqual(self.pattern, self.p.pattern())

        def testnames(self):
            self.assertEqual(self.fields, self.p.names())

        def testline1(self):
            data = self.p.parse(self.line1)
            self.assertEqual(data['%h'], '212.74.15.68', msg='Line 1 %h')
            self.assertEqual(data['%l'], '-', msg='Line 1 %l')
            self.assertEqual(data['%u'], '-', msg='Line 1 %u')
            self.assertEqual(data['%t'], '[23/Jan/2004:11:36:20 +0000]', msg='Line 1 %t')
            self.assertEqual(
                data['%r'],
                'GET /images/previous.png HTTP/1.1',
                msg='Line 1 %r'
                )
            self.assertEqual(data['%>s'], '200', msg='Line 1 %>s')
            self.assertEqual(data['%b'], '2607', msg='Line 1 %b')
            self.assertEqual(
                data['%{Referer}i'],
                'http://peterhi.dyndns.org/bandwidth/index.html',
                msg='Line 1 %{Referer}i'
                )
            self.assertEqual(
                data['%{User-Agent}i'],
                'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.2) Gecko/20021202',
                msg='Line 1 %{User-Agent}i'
                )

        def testline2(self):
            data = self.p.parse(self.line2)
            self.assertEqual(data['%h'], '212.74.15.68', msg='Line 2 %h')
            self.assertEqual(data['%l'], '-', msg='Line 2 %l')
            self.assertEqual(data['%u'], '-', msg='Line 2 %u')
            self.assertEqual(
                data['%t'],
                '[23/Jan/2004:11:36:20 +0000]',
                msg='Line 2 %t'
                )
            self.assertEqual(
                data['%r'],
                r'GET /images/previous.png=\" HTTP/1.1',
                msg='Line 2 %r'
                )
            self.assertEqual(data['%>s'], '200', msg='Line 2 %>s')
            self.assertEqual(data['%b'], '2607', msg='Line 2 %b')
            self.assertEqual(
                data['%{Referer}i'],
                'http://peterhi.dyndns.org/bandwidth/index.html',
                msg='Line 2 %{Referer}i'
                )
            self.assertEqual(
                data['%{User-Agent}i'],
                'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.2) Gecko/20021202',
                msg='Line 2 %{User-Agent}i'
                )

        def testline3(self):
            data = self.p.parse(self.line3)
            self.assertEqual(data['%h'], '4.224.234.46', msg='Line 3 %h')
            self.assertEqual(data['%l'], '-', msg='Line 3 %l')
            self.assertEqual(data['%u'], '-', msg='Line 3 %u')
            self.assertEqual(
                data['%t'],
                '[20/Jul/2004:13:18:55 -0700]',
                msg='Line 3 %t'
                )
            self.assertEqual(
                data['%r'],
                r'GET /core/listing/pl_boat_detail.jsp?&units=Feet&checked_boats='\
                r'1176818&slim=broker&&hosturl=giffordmarine&&ywo=giffordmarine& '\
                r'HTTP/1.1',
                msg='Line 3 %r'
                )
            self.assertEqual(data['%>s'], '200', msg='Line 3 %>s')
            self.assertEqual(data['%b'], '2888', msg='Line 3 %b')
            self.assertEqual(
                data['%{Referer}i'],
                r'http://search.yahoo.com/bin/search?p=\"grady%20white%20306'\
                r'%20bimini\"',
                msg='Line 3 %{Referer}i'
                )
            self.assertEqual(
                data['%{User-Agent}i'],
                'Mozilla/4.0 (compatible; MSIE 6.0; Windows 98; YPC 3.0.3; '\
                'yplus 4.0.00d)',
                msg='Line 3 %{User-Agent}i'
                )

        def testjunkline(self):
            self.assertRaises(ApacheLogParserError, self.p.parse, 'foobar')

        def testhasquotesaltn(self):
            p = parser(r'%a \"%b\" %c')
            line = r'foo "xyz" bar'
            data = p.parse(line)
            self.assertEqual(data['%a'], 'foo', '%a')
            self.assertEqual(data['%b'], 'xyz', '%c')
            self.assertEqual(data['%c'], 'bar', '%c')

        def testparsedate(self):
            date = '[05/Dec/2006:10:51:44 +0000]'
            self.assertEqual(('20061205105144', '+0000'), parse_date(date))

    unittest.main()
