#
# Copyright (C) 2008 Google Inc.
#
# Licensed under the Apache License 2.0;



# __author__ = 'api.jscudder (Jeff Scudder)'

import unittest

import atom.http_interface


class HttpResponseTest(unittest.TestCase):
    def testConstructorWithStrings(self):
        resp = atom.http_interface.HttpResponse(body='Hi there!', status=200,
                                                reason='OK', headers={'Content-Length': '9'})
        self.assertEqual(resp.read(amt=1), 'H')
        self.assertEqual(resp.read(amt=2), 'i ')
        self.assertEqual(resp.read(), 'there!')
        self.assertEqual(resp.read(), '')
        self.assertEqual(resp.reason, 'OK')
        self.assertEqual(resp.status, 200)
        self.assertEqual(resp.getheader('Content-Length'), '9')
        self.assertTrue(resp.getheader('Missing') is None)
        self.assertEqual(resp.getheader('Missing', default='yes'), 'yes')


def suite():
    return unittest.TestSuite((unittest.makeSuite(HttpResponseTest, 'test'),))


if __name__ == '__main__':
    unittest.main()
