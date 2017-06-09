#
# Copyright 2011 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License 2.0;


"""Data model tests for the Multidomain Provisioning API."""

# __author__ = 'Claudio Cherubino <ccherubino@google.com>'

import unittest

import atom.core
import gdata.apps.multidomain.data
import gdata.test_config as conf
from gdata import test_data


class UserEntryTest(unittest.TestCase):
    def setUp(self):
        self.entry = atom.core.parse(test_data.MULTIDOMAIN_USER_ENTRY,
                                     gdata.apps.multidomain.data.UserEntry)
        self.feed = atom.core.parse(test_data.MULTIDOMAIN_USER_FEED,
                                    gdata.apps.multidomain.data.UserFeed)

    def testUserEntryFromString(self):
        self.assertTrue(isinstance(self.entry,
                                   gdata.apps.multidomain.data.UserEntry))
        self.assertEqual(self.entry.first_name, 'Liz')
        self.assertEqual(self.entry.last_name, 'Smith')
        self.assertEqual(self.entry.email, 'liz@example.com')
        self.assertEqual(self.entry.password,
                         '51eea05d46317fadd5cad6787a8f562be90b4446')
        self.assertEqual(self.entry.is_admin, 'true')

    def testUserFeedFromString(self):
        self.assertEqual(len(self.feed.entry), 2)
        self.assertTrue(isinstance(self.feed,
                                   gdata.apps.multidomain.data.UserFeed))
        self.assertTrue(isinstance(self.feed.entry[0],
                                   gdata.apps.multidomain.data.UserEntry))
        self.assertTrue(isinstance(self.feed.entry[1],
                                   gdata.apps.multidomain.data.UserEntry))
        self.assertEqual(
            self.feed.entry[0].find_edit_link(),
            ('https://apps-apis.google.com/a/feeds/user/2.0/example.com/'
             'admin%40example.com'))
        self.assertEqual(self.feed.entry[0].first_name, 'Joe')
        self.assertEqual(self.feed.entry[0].last_name, 'Brown')
        self.assertEqual(self.feed.entry[0].email, 'admin@example.com')
        self.assertEqual(self.feed.entry[0].is_admin, 'true')
        self.assertEqual(self.feed.entry[0].suspended, 'false')
        self.assertEqual(self.feed.entry[0].change_password_at_next_login, 'false')
        self.assertEqual(self.feed.entry[0].ip_whitelisted, 'false')
        self.assertEqual(
            self.feed.entry[1].find_edit_link(),
            ('https://apps-apis.google.com/a/feeds/user/2.0/example.com/'
             'liz%40example.com'))
        self.assertEqual(self.feed.entry[1].first_name, 'Elizabeth')
        self.assertEqual(self.feed.entry[1].last_name, 'Smith')
        self.assertEqual(self.feed.entry[1].email, 'liz@example.com')
        self.assertEqual(self.feed.entry[1].is_admin, 'true')
        self.assertEqual(self.feed.entry[1].suspended, 'false')
        self.assertEqual(self.feed.entry[1].change_password_at_next_login, 'false')
        self.assertEqual(self.feed.entry[1].ip_whitelisted, 'false')


class UserRenameRequestTest(unittest.TestCase):
    def setUp(self):
        self.entry = atom.core.parse(test_data.MULTIDOMAIN_USER_RENAME_REQUEST,
                                     gdata.apps.multidomain.data.UserRenameRequest)

    def testUserRenameRequestFromString(self):
        self.assertTrue(isinstance(self.entry,
                                   gdata.apps.multidomain.data.UserRenameRequest))
        self.assertEqual(self.entry.new_email, 'liz@newexample4liz.com')


class AliasEntryTest(unittest.TestCase):
    def setUp(self):
        self.entry = atom.core.parse(test_data.MULTIDOMAIN_ALIAS_ENTRY,
                                     gdata.apps.multidomain.data.AliasEntry)
        self.feed = atom.core.parse(test_data.MULTIDOMAIN_ALIAS_FEED,
                                    gdata.apps.multidomain.data.AliasFeed)

    def testAliasEntryFromString(self):
        self.assertTrue(isinstance(self.entry,
                                   gdata.apps.multidomain.data.AliasEntry))
        self.assertEqual(self.entry.user_email, 'liz@example.com')
        self.assertEqual(self.entry.alias_email, 'helpdesk@gethelp_example.com')

    def testAliasFeedFromString(self):
        self.assertEqual(len(self.feed.entry), 2)
        self.assertTrue(isinstance(self.feed,
                                   gdata.apps.multidomain.data.AliasFeed))
        self.assertTrue(isinstance(self.feed.entry[0],
                                   gdata.apps.multidomain.data.AliasEntry))
        self.assertTrue(isinstance(self.feed.entry[1],
                                   gdata.apps.multidomain.data.AliasEntry))
        self.assertEqual(
            self.feed.entry[0].find_edit_link(),
            ('https://apps-apis.google.com/a/feeds/alias/2.0/gethelp_example.com/'
             'helpdesk%40gethelp_example.com'))
        self.assertEqual(self.feed.entry[0].user_email, 'liz@example.com')
        self.assertEqual(self.feed.entry[0].alias_email,
                         'helpdesk@gethelp_example.com')
        self.assertEqual(
            self.feed.entry[1].find_edit_link(),
            ('https://apps-apis.google.com/a/feeds/alias/2.0/gethelp_example.com/'
             'support%40gethelp_example.com'))
        self.assertEqual(self.feed.entry[1].user_email, 'joe@example.com')
        self.assertEqual(self.feed.entry[1].alias_email,
                         'support@gethelp_example.com')


def suite():
    return conf.build_suite([UserEntryTest, AliasEntryTest])


if __name__ == '__main__':
    unittest.main()
