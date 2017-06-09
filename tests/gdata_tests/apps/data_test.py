#
# Copyright 2011 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License 2.0;


"""Data model tests for the Provisioning API."""

# __author__ = 'Shraddha Gupta <shraddhag@google.com>'

import unittest

import atom.core
import gdata.apps.data
import gdata.test_config as conf
from gdata import test_data


class UserEntryTest(unittest.TestCase):
    def setUp(self):
        self.entry = atom.core.parse(test_data.USER_ENTRY1,
                                     gdata.apps.data.UserEntry)
        self.feed = atom.core.parse(test_data.USER_FEED1,
                                    gdata.apps.data.UserFeed)

    def testUserEntryFromString(self):
        self.assertTrue(isinstance(self.entry,
                                   gdata.apps.data.UserEntry))
        self.assertEqual(self.entry.name.given_name, 'abcd33')
        self.assertEqual(self.entry.name.family_name, 'efgh3')
        self.assertEqual(self.entry.login.user_name, 'abcd12310')
        self.assertEqual(self.entry.login.suspended, 'false')
        self.assertEqual(self.entry.login.admin, 'false')
        self.assertEqual(self.entry.quota.limit, '25600')

    def testUserFeedFromString(self):
        self.assertEqual(len(self.feed.entry), 2)
        self.assertTrue(isinstance(self.feed, gdata.apps.data.UserFeed))
        self.assertTrue(isinstance(self.feed.entry[0], gdata.apps.data.UserEntry))
        self.assertTrue(isinstance(self.feed.entry[1], gdata.apps.data.UserEntry))
        self.assertEqual(self.feed.entry[0].find_edit_link(),
                         ('https://apps-apis.google.com/a/feeds/srkapps.com/user/2.0/user8306'))
        self.assertEqual(self.feed.entry[0].name.given_name, 'FirstName8306')
        self.assertEqual(self.feed.entry[0].name.family_name, 'LastName8306')
        self.assertEqual(self.feed.entry[0].login.user_name, 'user8306')
        self.assertEqual(self.feed.entry[0].login.admin, 'false')
        self.assertEqual(self.feed.entry[0].login.suspended, 'false')
        self.assertEqual(self.feed.entry[0].login.change_password, 'false')
        self.assertEqual(self.feed.entry[0].login.ip_whitelisted, 'false')
        self.assertEqual(self.feed.entry[0].quota.limit, '25600')
        self.assertEqual(
            self.feed.entry[1].find_edit_link(),
            ('https://apps-apis.google.com/a/feeds/srkapps.com/user/2.0/user8307'))
        self.assertEqual(self.feed.entry[1].name.given_name, 'FirstName8307')
        self.assertEqual(self.feed.entry[1].name.family_name, 'LastName8307')
        self.assertEqual(self.feed.entry[1].login.user_name, 'user8307')
        self.assertEqual(self.feed.entry[1].login.admin, 'false')
        self.assertEqual(self.feed.entry[1].login.suspended, 'false')
        self.assertEqual(self.feed.entry[1].login.change_password, 'false')
        self.assertEqual(self.feed.entry[1].login.ip_whitelisted, 'false')
        self.assertEqual(self.feed.entry[1].quota.limit, '25600')


class NicknameEntryTest(unittest.TestCase):
    def setUp(self):
        self.entry = atom.core.parse(test_data.NICKNAME_ENTRY,
                                     gdata.apps.data.NicknameEntry)
        self.feed = atom.core.parse(test_data.NICKNAME_FEED,
                                    gdata.apps.data.NicknameFeed)

    def testNicknameEntryFromString(self):
        self.assertTrue(isinstance(self.entry,
                                   gdata.apps.data.NicknameEntry))
        self.assertEqual(self.entry.nickname.name, 'nehag')
        self.assertEqual(self.entry.login.user_name, 'neha')

    def testNicknameFeedFromString(self):
        self.assertEqual(len(self.feed.entry), 2)
        self.assertTrue(isinstance(self.feed,
                                   gdata.apps.data.NicknameFeed))
        self.assertTrue(isinstance(self.feed.entry[0],
                                   gdata.apps.data.NicknameEntry))
        self.assertTrue(isinstance(self.feed.entry[1],
                                   gdata.apps.data.NicknameEntry))
        self.assertEqual(
            self.feed.entry[0].find_edit_link(),
            ('https://apps-apis.google.com/a/feeds/srkapps.net/'
             'nickname/2.0/nehag'))
        self.assertEqual(self.feed.entry[0].nickname.name, 'nehag')
        self.assertEqual(self.feed.entry[0].login.user_name, 'neha')
        self.assertEqual(
            self.feed.entry[1].find_edit_link(),
            ('https://apps-apis.google.com/a/feeds/srkapps.net/'
             'nickname/2.0/richag'))
        self.assertEqual(self.feed.entry[1].nickname.name, 'richag')
        self.assertEqual(self.feed.entry[1].login.user_name, 'richa')


def suite():
    return conf.build_suite([UserEntryTest, NicknameEntryTest])


if __name__ == '__main__':
    unittest.main()
