#
# Copyright (C) 2006 Google Inc.
#
# Licensed under the Apache License 2.0;


# __author__ = 'j.s@google.com (Jeff Scudder)'

import os
import unittest

import atom.mock_http_core
import atom.service
import gdata.test_config as conf


class AtomServiceUnitTest(unittest.TestCase):
    def testBuildUriWithNoParams(self):
        x = atom.service.BuildUri('/base/feeds/snippets')
        self.assertTrue(x == '/base/feeds/snippets')

    def testBuildUriWithParams(self):
        # Add parameters to a URI
        x = atom.service.BuildUri('/base/feeds/snippets', url_params={'foo': 'bar',
                                                                      'bq': 'digital camera'})
        self.assertTrue(x == '/base/feeds/snippets?foo=bar&bq=digital+camera')
        self.assertTrue(x.startswith('/base/feeds/snippets'))
        self.assertTrue(x.count('?') == 1)
        self.assertTrue(x.count('&') == 1)
        self.assertTrue(x.index('?') < x.index('&'))
        self.assertTrue(x.index('bq=digital+camera') != -1)

        # Add parameters to a URI that already has parameters
        x = atom.service.BuildUri('/base/feeds/snippets?bq=digital+camera',
                                  url_params={'foo': 'bar', 'max-results': '250'})
        self.assertTrue(x.startswith('/base/feeds/snippets?bq=digital+camera'))
        self.assertTrue(x.count('?') == 1)
        self.assertTrue(x.count('&') == 2)
        self.assertTrue(x.index('?') < x.index('&'))
        self.assertTrue(x.index('max-results=250') != -1)
        self.assertTrue(x.index('foo=bar') != -1)

    def testBuildUriWithoutParameterEscaping(self):
        x = atom.service.BuildUri('/base/feeds/snippets',
                                  url_params={'foo': ' bar', 'bq': 'digital camera'},
                                  escape_params=False)
        self.assertTrue(x.index('foo= bar') != -1)
        self.assertTrue(x.index('bq=digital camera') != -1)

    def testParseHttpUrl(self):
        atom_service = atom.service.AtomService('code.google.com')
        self.assertEqual(atom_service.server, 'code.google.com')
        (host, port, ssl, path) = atom.service.ProcessUrl(atom_service,
                                                          'http://www.google.com/service/subservice?name=value')

        self.assertEqual(ssl, False)
        self.assertEqual(host, 'www.google.com')
        self.assertEqual(port, 80)
        self.assertEqual(path, '/service/subservice?name=value')

    def testParseHttpUrlWithPort(self):
        atom_service = atom.service.AtomService('code.google.com')
        self.assertEqual(atom_service.server, 'code.google.com')
        (host, port, ssl, path) = atom.service.ProcessUrl(atom_service,
                                                          'http://www.google.com:12/service/subservice?name=value&newname=newvalue')

        self.assertEqual(ssl, False)
        self.assertEqual(host, 'www.google.com')
        self.assertEqual(port, 12)
        self.assertTrue(path.startswith('/service/subservice?'))
        self.assertTrue(path.find('name=value') >= len('/service/subservice?'))
        self.assertTrue(path.find('newname=newvalue') >= len('/service/subservice?'))

    def testParseHttpsUrl(self):
        atom_service = atom.service.AtomService('code.google.com')
        self.assertEqual(atom_service.server, 'code.google.com')
        (host, port, ssl, path) = atom.service.ProcessUrl(atom_service,
                                                          'https://www.google.com/service/subservice?name=value&newname=newvalue')

        self.assertEqual(ssl, True)
        self.assertEqual(host, 'www.google.com')
        self.assertEqual(port, 443)
        self.assertTrue(path.startswith('/service/subservice?'))
        self.assertTrue(path.find('name=value') >= len('/service/subservice?'))
        self.assertTrue(path.find('newname=newvalue') >= len('/service/subservice?'))

    def testParseHttpsUrlWithPort(self):
        atom_service = atom.service.AtomService('code.google.com')
        self.assertEqual(atom_service.server, 'code.google.com')
        (host, port, ssl, path) = atom.service.ProcessUrl(atom_service,
                                                          'https://www.google.com:13981/service/subservice?name=value&newname=newvalue')

        self.assertEqual(ssl, True)
        self.assertEqual(host, 'www.google.com')
        self.assertEqual(port, 13981)
        self.assertTrue(path.startswith('/service/subservice?'))
        self.assertTrue(path.find('name=value') >= len('/service/subservice?'))
        self.assertTrue(path.find('newname=newvalue') >= len('/service/subservice?'))

    def testSetBasicAuth(self):
        client = atom.service.AtomService()
        client.UseBasicAuth('foo', 'bar')
        token = client.token_store.find_token('http://')
        self.assertTrue(isinstance(token, atom.service.BasicAuthToken))
        self.assertEqual(token.auth_header, 'Basic Zm9vOmJhcg==')
        client.UseBasicAuth('', '')
        token = client.token_store.find_token('http://')
        self.assertTrue(isinstance(token, atom.service.BasicAuthToken))
        self.assertEqual(token.auth_header, 'Basic Og==')

    def testProcessUrlWithStringForService(self):
        (server, port, ssl, uri) = atom.service.ProcessUrl(
            service='www.google.com', url='/base/feeds/items')
        self.assertEqual(server, 'www.google.com')
        self.assertEqual(port, 80)
        self.assertEqual(ssl, False)
        self.assertTrue(uri.startswith('/base/feeds/items'))

        client = atom.service.AtomService()
        client.server = 'www.google.com'
        client.ssl = True
        (server, port, ssl, uri) = atom.service.ProcessUrl(
            service=client, url='/base/feeds/items')
        self.assertEqual(server, 'www.google.com')
        self.assertEqual(ssl, True)
        self.assertTrue(uri.startswith('/base/feeds/items'))

        (server, port, ssl, uri) = atom.service.ProcessUrl(service=None,
                                                           url='https://www.google.com/base/feeds/items')
        self.assertEqual(server, 'www.google.com')
        self.assertEqual(port, 443)
        self.assertEqual(ssl, True)
        self.assertTrue(uri.startswith('/base/feeds/items'))

    def testHostHeaderContainsNonDefaultPort(self):
        client = atom.service.AtomService()
        client.http_client.v2_http_client = atom.mock_http_core.EchoHttpClient()
        response = client.Get('http://example.com')
        self.assertEqual(response.getheader('Echo-Host'), 'example.com:None')
        response = client.Get('https://example.com')
        self.assertEqual(response.getheader('Echo-Host'), 'example.com:None')
        response = client.Get('https://example.com:8080')
        self.assertEqual(response.getheader('Echo-Host'), 'example.com:8080')
        response = client.Get('http://example.com:1234')
        self.assertEqual(response.getheader('Echo-Host'), 'example.com:1234')

    def testBadHttpsProxyRaisesRealException(self):
        """Test that real exceptions are raised when there is an error connecting to
        a host with an https proxy
        """
        client = atom.service.AtomService(server='example.com')
        client.server = 'example.com'
        os.environ['https_proxy'] = 'http://example.com'
        self.assertRaises(atom.http.ProxyError,
                          atom.service.PrepareConnection, client, 'https://example.com')


def suite():
    return conf.build_suite([AtomServiceUnitTest])


if __name__ == '__main__':
    unittest.main()
