#
# Copyright (C) 2008 Google Inc.
#
# Licensed under the Apache License 2.0;



# __author__ = 'api.jscudder (Jeff Scudder)'

import unittest

import atom.mock_service
import gdata.service

gdata.service.http_request_handler = atom.mock_service


class MockRequestTest(unittest.TestCase):
    def setUp(self):
        self.request_thumbprint = atom.mock_service.MockRequest('GET',
                                                                'http://www.google.com',
                                                                extra_headers={'Header1': 'a', 'Header2': 'b'})

    def testIsMatch(self):
        matching_request = atom.mock_service.MockRequest('GET',
                                                         'http://www.google.com', extra_headers={'Header1': 'a',
                                                                                                 'Header2': 'b', 'Header3': 'c'})
        bad_url = atom.mock_service.MockRequest('GET', 'http://example.com',
                                                extra_headers={'Header1': 'a', 'Header2': 'b', 'Header3': 'c'})
        # Should match because we don't check headers at the moment.
        bad_header = atom.mock_service.MockRequest('GET',
                                                   'http://www.google.com', extra_headers={'Header1': 'a',
                                                                                           'Header2': '1', 'Header3': 'c'})
        bad_verb = atom.mock_service.MockRequest('POST', 'http://www.google.com',
                                                 data='post data', extra_headers={'Header1': 'a', 'Header2': 'b'})
        self.assertEqual(self.request_thumbprint.IsMatch(matching_request), True)
        self.assertEqual(self.request_thumbprint.IsMatch(bad_url), False)
        self.assertEqual(self.request_thumbprint.IsMatch(bad_header), True)
        self.assertEqual(self.request_thumbprint.IsMatch(bad_verb), False)


class HttpRequestTest(unittest.TestCase):
    def setUp(self):
        atom.mock_service.recordings = []
        self.client = gdata.service.GDataService()

    def testSimpleRecordedGet(self):
        recorded_request = atom.mock_service.MockRequest('GET', 'http://example.com/')
        recorded_response = atom.mock_service.MockHttpResponse('Got it', 200,
                                                               'OK')
        # Add a tuple mapping the mock request to the mock response
        atom.mock_service.recordings.append((recorded_request, recorded_response))
        # Try a couple of GET requests which should match the recorded request.
        response = self.client.Get('http://example.com/', converter=str)
        self.assertEqual(response, 'Got it')

        self.client.server = 'example.com'
        raw_response = self.client.handler.HttpRequest(self.client, 'GET', None,
                                                       '/')
        self.assertEqual(raw_response.read(), 'Got it')
        self.assertEqual(raw_response.status, 200)
        self.assertEqual(raw_response.reason, 'OK')


class RecordRealHttpRequestsTest(unittest.TestCase):
    def testRecordAndReuseResponse(self):
        client = gdata.service.GDataService()
        client.server = 'www.google.com'
        atom.mock_service.recordings = []
        atom.mock_service.real_request_handler = atom.service

        # Record a response
        real_response = atom.mock_service.HttpRequest(client, 'GET', None, 'http://www.google.com/')
        # Enter 'replay' mode
        atom.mock_service.real_request_handler = None
        mock_response = atom.mock_service.HttpRequest(client, 'GET', None, 'http://www.google.com/')
        self.assertEqual(real_response.reason, mock_response.reason)
        self.assertEqual(real_response.status, mock_response.status)
        self.assertEqual(real_response.read(), mock_response.read())


if __name__ == '__main__':
    unittest.main()
