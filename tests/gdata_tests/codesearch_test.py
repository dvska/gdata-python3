#
# Copyright (C) 2007 Google Inc.
#
# Licensed under the Apache License 2.0;



# __author__ = 'api.jscudder (Jeffrey Scudder)'

import unittest

import gdata.codesearch
import gdata.test_data


class CodeSearchDataTest(unittest.TestCase):
    def setUp(self):
        self.feed = gdata.codesearch.CodesearchFeedFromString(
            gdata.test_data.CODE_SEARCH_FEED)

    def testCorrectXmlConversion(self):
        self.assertTrue(self.feed.id.text ==
                        'http://www.google.com/codesearch/feeds/search?q=malloc')
        self.assertTrue(len(self.feed.entry) == 10)
        for entry in self.feed.entry:
            if entry.id.text == ('http://www.google.com/codesearch?hl=en&q=+ma'
                                 'lloc+show:LDjwp-Iqc7U:84hEYaYsZk8:xDGReDhvNi0&sa=N&ct=rx&cd=1'
                                 '&cs_p=http://www.gnu.org&cs_f=software/autoconf/manual/autoco'
                                 'nf-2.60/autoconf.html-002&cs_p=http://www.gnu.org&cs_f=softwa'
                                 're/autoconf/manual/autoconf-2.60/autoconf.html-002#first'):
                self.assertTrue(len(entry.match) == 4)
                for match in entry.match:
                    if match.line_number == '4':
                        self.assertTrue(match.type == 'text/html')
                self.assertTrue(entry.file.name ==
                                'software/autoconf/manual/autoconf-2.60/autoconf.html-002')
                self.assertTrue(entry.package.name == 'http://www.gnu.org')
                self.assertTrue(entry.package.uri == 'http://www.gnu.org')


if __name__ == '__main__':
    unittest.main()
