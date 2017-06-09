#
# Copyright (C) 2008 Google Inc.
#
# Licensed under the Apache License 2.0;



# __author__ = 'j.s@google.com (Jeff Scudder)'

import unittest

import atom.http
import atom.mock_http


class MockHttpClientUnitTest(unittest.TestCase):
    def setUp(self):
        self.client = atom.mock_http.MockHttpClient()

    def testRepondToGet(self):
        mock_response = atom.http_interface.HttpResponse(body='Hooray!',
                                                         status=200, reason='OK')
        self.client.add_response(mock_response, 'GET',
                                 'http://example.com/hooray')

        response = self.client.request('GET', 'http://example.com/hooray')

        self.assertEqual(len(self.client.recordings), 1)
        self.assertEqual(response.status, 200)
        self.assertEqual(response.read(), 'Hooray!')

    def testRecordResponse(self):
        # Turn on pass-through record mode.
        self.client.real_client = atom.http.ProxiedHttpClient()
        live_response = self.client.request('GET',
                                            'https://www.blogger.com/feeds/7986894085536788407/posts/default?max-results=1')
        live_response_body = live_response.read()
        self.assertEqual(live_response.status, 200)
        self.assertEqual(live_response_body.startswith('<?xml'), True)

        # Requery for the now canned data.
        self.client.real_client = None
        canned_response = self.client.request('GET',
                                              'https://www.blogger.com/feeds/7986894085536788407/posts/default?max-results=1')

        # The canned response should be the stored response.
        canned_response_body = canned_response.read()
        self.assertEqual(canned_response.status, 200)
        self.assertEqual(canned_response_body, live_response_body)

    def testUnrecordedRequest(self):
        try:
            self.client.request('POST', 'http://example.org')
            self.fail()
        except atom.mock_http.NoRecordingFound:
            pass


def suite():
    return unittest.TestSuite(
        (unittest.makeSuite(MockHttpClientUnitTest, 'test'),))


if __name__ == '__main__':
    unittest.main()
