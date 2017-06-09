#!/usr/bin/env python
#
# Copyright (C) 2009 Google Inc.
#
# Licensed under the Apache License 2.0;



# This module is used for version 2 of the Google Data APIs.
# These tests attempt to connect to Google servers.


# __author__ = 'jcgregorio@google.com (Joe Gregorio)'

import unittest

import atom.core
import atom.data
import atom.http_core
import gdata.contacts.client
import gdata.data
import gdata.test_config as conf

conf.options.register_option(conf.APPS_DOMAIN_OPTION)
conf.options.register_option(conf.TARGET_USERNAME_OPTION)


class ProfileTest(unittest.TestCase):
    def setUp(self):
        self.client = gdata.contacts.client.ContactsClient(domain='example.com')
        if conf.options.get_value('runlive') == 'true':
            self.client = gdata.contacts.client.ContactsClient(
                domain=conf.options.get_value('appsdomain'))
            if conf.options.get_value('ssl') == 'true':
                self.client.ssl = True
            conf.configure_client(self.client, 'ProfileTest',
                                  self.client.auth_service, True)
            self.client.username = conf.options.get_value('appsusername').split('@')[0]

    def tearDown(self):
        conf.close_client(self.client)

    def test_profiles_feed(self):
        if not conf.options.get_value('runlive') == 'true':
            return
        # Either load the recording or prepare to make a live request.
        conf.configure_cache(self.client, 'test_profiles_feed')

        feed = self.client.get_profiles_feed()
        self.assertTrue(isinstance(feed, gdata.contacts.data.ProfilesFeed))

    def test_profiles_query(self):
        if not conf.options.get_value('runlive') == 'true':
            return
        # Either load the recording or prepare to make a live request.
        conf.configure_cache(self.client, 'test_profiles_feed')

        query = gdata.contacts.client.ProfilesQuery(max_results=1)
        feed = self.client.get_profiles_feed(q=query)
        self.assertTrue(isinstance(feed, gdata.contacts.data.ProfilesFeed))
        self.assertTrue(len(feed.entry) == 1)

        # Needs at least 2 profiles in the feed to test the start-key
        # query param.
        next = feed.GetNextLink()
        feed = None
        if next:
            # Retrieve the start-key query param from the next link.
            uri = atom.http_core.Uri.parse_uri(next.href)
            if 'start-key' in uri.query:
                query.start_key = uri.query['start-key']
                feed = self.client.get_profiles_feed(q=query)
                self.assertTrue(isinstance(feed, gdata.contacts.data.ProfilesFeed))
                self.assertTrue(len(feed.entry) == 1)
                self.assertTrue(feed.GetSelfLink().href == next.href)
                # Compare with a feed retrieved with the next link.
                next_feed = self.client.get_profiles_feed(uri=next.href)
                self.assertTrue(len(next_feed.entry) == 1)
                self.assertTrue(next_feed.entry[0].id.text == feed.entry[0].id.text)


def suite():
    return conf.build_suite([ProfileTest])


if __name__ == '__main__':
    unittest.TextTestRunner().run(suite())
