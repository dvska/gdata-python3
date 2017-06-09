#
# Copyright (C) 2008 Google Inc.
#
# Licensed under the Apache License 2.0;



# __author__ = 'j.s@google.com (Jeff Scudder)'

import unittest

import atom.http_interface
import atom.service
import atom.token_store
import atom.url


class TokenStoreTest(unittest.TestCase):
    def setUp(self):
        self.token = atom.service.BasicAuthToken('aaa1', scopes=[
            'http://example.com/', 'http://example.org'])
        self.tokens = atom.token_store.TokenStore()
        self.tokens.add_token(self.token)

    def testAddAndFindTokens(self):
        self.assertTrue(self.tokens.find_token('http://example.com/') == self.token)
        self.assertTrue(self.tokens.find_token('http://example.org/') == self.token)
        self.assertTrue(self.tokens.find_token('http://example.org/foo?ok=1') == (
            self.token))
        self.assertTrue(isinstance(self.tokens.find_token('http://example.net/'),
                                   atom.http_interface.GenericToken))
        self.assertTrue(isinstance(self.tokens.find_token('example.com/'),
                                   atom.http_interface.GenericToken))

    def testFindTokenUsingMultipleUrls(self):
        self.assertTrue(self.tokens.find_token(
            'http://example.com/') == self.token)
        self.assertTrue(self.tokens.find_token(
            'http://example.org/bar') == self.token)
        self.assertTrue(isinstance(self.tokens.find_token(''),
                                   atom.http_interface.GenericToken))
        self.assertTrue(isinstance(self.tokens.find_token(
            'http://example.net/'),
            atom.http_interface.GenericToken))

    def testFindTokenWithPartialScopes(self):
        token = atom.service.BasicAuthToken('aaa1',
                                            scopes=[atom.url.Url(host='www.example.com', path='/foo'),
                                                    atom.url.Url(host='www.example.net')])
        token_store = atom.token_store.TokenStore()
        token_store.add_token(token)
        self.assertTrue(token_store.find_token(
            'http://www.example.com/foobar') == token)
        self.assertTrue(token_store.find_token(
            'https://www.example.com:443/foobar') == token)
        self.assertTrue(token_store.find_token(
            'http://www.example.net/xyz') == token)
        self.assertTrue(token_store.find_token('http://www.example.org/') != token)
        self.assertTrue(isinstance(token_store.find_token('http://example.org/'),
                                   atom.http_interface.GenericToken))


def suite():
    return unittest.TestSuite((unittest.makeSuite(TokenStoreTest, 'test'),))


if __name__ == '__main__':
    unittest.main()
