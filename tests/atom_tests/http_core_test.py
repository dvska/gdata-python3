#!/usr/bin/env python
#
#    Copyright (C) 2009 Google Inc.
#
#   Licensed under the Apache License 2.0;
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.


# This module is used for version 2 of the Google Data APIs.


# __author__ = 'j.s@google.com (Jeff Scudder)'

import io
import unittest

import atom.http_core


class UriTest(unittest.TestCase):
    def test_parse_uri(self):
        uri = atom.http_core.parse_uri('http://www.google.com/test?q=foo&z=bar')
        self.assertTrue(uri.scheme == 'http')
        self.assertTrue(uri.host == 'www.google.com')
        self.assertTrue(uri.port is None)
        self.assertTrue(uri.path == '/test')
        self.assertTrue(uri.query == {'z': 'bar', 'q': 'foo'})

    def test_static_parse_uri(self):
        uri = atom.http_core.Uri.parse_uri('http://test.com/?token=foo&x=1')
        self.assertEqual(uri.scheme, 'http')
        self.assertEqual(uri.host, 'test.com')
        self.assertTrue(uri.port is None)
        self.assertEqual(uri.query, {'token': 'foo', 'x': '1'})

    def test_modify_request_no_request(self):
        uri = atom.http_core.parse_uri('http://www.google.com/test?q=foo&z=bar')
        request = uri.modify_request()
        self.assertTrue(request.uri.scheme == 'http')
        self.assertTrue(request.uri.host == 'www.google.com')
        # If no port was provided, the HttpClient is responsible for determining
        # the default.
        self.assertTrue(request.uri.port is None)
        self.assertTrue(request.uri.path.startswith('/test'))
        self.assertEqual(request.uri.query, {'z': 'bar', 'q': 'foo'})
        self.assertTrue(request.method is None)
        self.assertTrue(request.headers == {})
        self.assertTrue(request._body_parts == [])

    def test_modify_request_http_with_set_port(self):
        request = atom.http_core.HttpRequest(uri=atom.http_core.Uri(port=8080),
                                             method='POST')
        request.add_body_part('hello', 'text/plain')
        uri = atom.http_core.parse_uri('//example.com/greet')
        self.assertTrue(uri.query == {})
        self.assertTrue(uri._get_relative_path() == '/greet')
        self.assertTrue(uri.host == 'example.com')
        self.assertTrue(uri.port is None)

        uri.ModifyRequest(request)
        self.assertTrue(request.uri.host == 'example.com')
        # If no scheme was provided, the URI will not add one, but the HttpClient
        # should assume the request is HTTP.
        self.assertTrue(request.uri.scheme is None)
        self.assertTrue(request.uri.port == 8080)
        self.assertTrue(request.uri.path == '/greet')
        self.assertTrue(request.method == 'POST')
        self.assertTrue(request.headers['Content-Type'] == 'text/plain')

    def test_modify_request_use_default_ssl_port(self):
        request = atom.http_core.HttpRequest(
            uri=atom.http_core.Uri(scheme='https'), method='PUT')
        request.add_body_part('hello', 'text/plain')
        uri = atom.http_core.parse_uri('/greet')
        uri.modify_request(request)
        self.assertTrue(request.uri.host is None)
        self.assertTrue(request.uri.scheme == 'https')
        # If no port was provided, leave the port as None, it is up to the
        # HttpClient to set the correct default port.
        self.assertTrue(request.uri.port is None)
        self.assertTrue(request.uri.path == '/greet')
        self.assertTrue(request.method == 'PUT')
        self.assertTrue(request.headers['Content-Type'] == 'text/plain')
        self.assertTrue(len(request._body_parts) == 1)
        self.assertTrue(request._body_parts[0] == 'hello')

    def test_to_string(self):
        uri = atom.http_core.Uri(host='www.google.com', query={'q': 'sippycode'})
        uri_string = uri._to_string()
        self.assertTrue(uri_string == 'http://www.google.com/?q=sippycode')


class HttpRequestTest(unittest.TestCase):
    def test_request_with_one_body_part(self):
        request = atom.http_core.HttpRequest()
        self.assertTrue(len(request._body_parts) == 0)
        self.assertTrue('Content-Length' not in request.headers)
        self.assertTrue(not 'Content-Type' in request.headers)
        self.assertTrue(not 'Content-Length' in request.headers)
        request.add_body_part('this is a test', 'text/plain')
        self.assertTrue(len(request._body_parts) == 1)
        self.assertTrue(request.headers['Content-Type'] == 'text/plain')
        self.assertTrue(request._body_parts[0] == 'this is a test')
        self.assertTrue(request.headers['Content-Length'] == str(len(
            'this is a test')))

    def test_add_file_without_size(self):
        virtual_file = io.StringIO('this is a test')
        request = atom.http_core.HttpRequest()
        try:
            request.add_body_part(virtual_file, 'text/plain')
            self.fail('We should have gotten an UnknownSize error.')
        except atom.http_core.UnknownSize:
            pass
        request.add_body_part(virtual_file, 'text/plain', len('this is a test'))
        self.assertTrue(len(request._body_parts) == 1)
        self.assertTrue(request.headers['Content-Type'] == 'text/plain')
        self.assertTrue(request._body_parts[0].read() == 'this is a test')
        self.assertTrue(request.headers['Content-Length'] == str(len(
            'this is a test')))

    def test_copy(self):
        request = atom.http_core.HttpRequest(
            uri=atom.http_core.Uri(scheme='https', host='www.google.com'),
            method='POST', headers={'test': '1', 'ok': 'yes'})
        request.add_body_part('body1', 'text/plain')
        request.add_body_part('<html>body2</html>', 'text/html')
        copied = request._copy()
        self.assertTrue(request.uri.scheme == copied.uri.scheme)
        self.assertTrue(request.uri.host == copied.uri.host)
        self.assertTrue(request.method == copied.method)
        self.assertTrue(request.uri.path == copied.uri.path)
        self.assertTrue(request.headers == copied.headers)
        self.assertTrue(request._body_parts == copied._body_parts)
        copied.headers['test'] = '2'
        copied._body_parts[1] = '<html>body3</html>'
        self.assertTrue(request.headers != copied.headers)
        self.assertTrue(request._body_parts != copied._body_parts)


def suite():
    return unittest.TestSuite((unittest.makeSuite(UriTest, 'test'),
                               unittest.makeSuite(HttpRequestTest, 'test')))


if __name__ == '__main__':
    unittest.main()
