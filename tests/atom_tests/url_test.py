#
# Copyright (C) 2008 Google Inc.
#
# Licensed under the Apache License 2.0;



# __author__ = 'j.s@google.com (Jeff Scudder)'

import unittest

import atom.url
import gdata.test_config as conf


class UrlTest(unittest.TestCase):
    def testParseUrl(self):
        url = atom.url.parse_url('http://www.google.com/calendar/feeds')
        self.assertTrue(url.protocol == 'http')
        self.assertTrue(url.port is None)
        self.assertTrue(url.host == 'www.google.com')
        self.assertTrue(url.path == '/calendar/feeds')
        self.assertTrue(url.params == {})

        url = atom.url.parse_url('http://example.com:6091/calendar/feeds')
        self.assertTrue(url.protocol == 'http')
        self.assertTrue(url.host == 'example.com')
        self.assertTrue(url.port == '6091')
        self.assertTrue(url.path == '/calendar/feeds')
        self.assertTrue(url.params == {})

        url = atom.url.parse_url('/calendar/feeds?foo=bar')
        self.assertTrue(url.protocol is None)
        self.assertTrue(url.host is None)
        self.assertTrue(url.path == '/calendar/feeds')
        self.assertTrue(len(list(url.params.keys())) == 1)
        self.assertTrue('foo' in url.params)
        self.assertTrue(url.params['foo'] == 'bar')

        url = atom.url.parse_url('/calendar/feeds?my+foo=bar%3Dx')
        self.assertTrue(len(list(url.params.keys())) == 1)
        self.assertTrue('my foo' in url.params)
        self.assertTrue(url.params['my foo'] == 'bar=x')

    def testUrlToString(self):
        url = atom.url.Url(port=80)
        url.host = 'example.com'
        self.assertTrue(str(url), '//example.com:80')

        url = atom.url.Url(protocol='http', host='example.com', path='/feed')
        url.params['has spaces'] = 'sneaky=values?&!'
        self.assertTrue(url.to_string() == (
            'http://example.com/feed?has+spaces=sneaky%3Dvalues%3F%26%21'))

    def testGetRequestUri(self):
        url = atom.url.Url(protocol='http', host='example.com', path='/feed')
        url.params['has spaces'] = 'sneaky=values?&!'
        self.assertTrue(url.get_request_uri() == (
            '/feed?has+spaces=sneaky%3Dvalues%3F%26%21'))
        self.assertTrue(url.get_param_string() == (
            'has+spaces=sneaky%3Dvalues%3F%26%21'))

    def testComparistons(self):
        url1 = atom.url.Url(protocol='http', host='example.com', path='/feed',
                            params={'x': '1', 'y': '2'})
        url2 = atom.url.Url(host='example.com', port=80, path='/feed',
                            params={'y': '2', 'x': '1'})
        self.assertEqual(url1, url2)
        url3 = atom.url.Url(host='example.com', port=81, path='/feed',
                            params={'x': '1', 'y': '2'})
        self.assertTrue(url1 != url3)
        self.assertTrue(url2 != url3)
        url4 = atom.url.Url(protocol='ftp', host='example.com', path='/feed',
                            params={'x': '1', 'y': '2'})
        self.assertTrue(url1 != url4)
        self.assertTrue(url2 != url4)
        self.assertTrue(url3 != url4)


def suite():
    return conf.build_suite([UrlTest])


if __name__ == '__main__':
    unittest.main()
