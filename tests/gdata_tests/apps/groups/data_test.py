#
# Copyright 2011 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License 2.0;


"""Data model tests for the Groups Provisioning API."""

# __author__ = 'Shraddha gupta <shraddhag@google.com>'

import unittest

import atom.core
import gdata.apps.groups.data
import gdata.test_config as conf
from gdata import test_data


class GroupEntryTest(unittest.TestCase):
    def setUp(self):
        self.entry = atom.core.parse(test_data.GROUP_ENTRY,
                                     gdata.apps.groups.data.GroupEntry, 2)
        self.feed = atom.core.parse(test_data.GROUP_FEED,
                                    gdata.apps.groups.data.GroupFeed, 2)

    def testGroupEntryFromString(self):
        self.assertTrue(isinstance(self.entry,
                                   gdata.apps.groups.data.GroupEntry))
        self.assertEqual(self.entry.group_id, 'trial@srkapps.com')
        self.assertEqual(self.entry.group_name, 'Trial')
        self.assertEqual(self.entry.email_permission, 'Domain')
        self.assertEqual(self.entry.description, 'For try')

    def testGroupFeedFromString(self):
        self.assertEqual(len(self.feed.entry), 2)
        self.assertTrue(isinstance(self.feed,
                                   gdata.apps.groups.data.GroupFeed))
        self.assertTrue(isinstance(self.feed.entry[0],
                                   gdata.apps.groups.data.GroupEntry))
        self.assertTrue(isinstance(self.feed.entry[1],
                                   gdata.apps.groups.data.GroupEntry))
        self.assertEqual(
            self.feed.entry[0].find_edit_link(),
            ('http://apps-apis.google.com/a/feeds/group/2.0/srkapps.com/'
             'firstgroup%40srkapps.com'))
        self.assertEqual(self.feed.entry[0].group_id, 'firstgroup@srkapps.com')
        self.assertEqual(self.feed.entry[0].group_name, 'FirstGroup')
        self.assertEqual(self.feed.entry[0].email_permission, 'Domain')
        self.assertEqual(self.feed.entry[0].description, 'First group')
        self.assertEqual(
            self.feed.entry[1].find_edit_link(),
            ('http://apps-apis.google.com/a/feeds/group/2.0/srkapps.com/'
             'trial%40srkapps.com'))
        self.assertEqual(self.feed.entry[1].group_id, 'trial@srkapps.com')
        self.assertEqual(self.feed.entry[1].group_name, 'Trial')
        self.assertEqual(self.feed.entry[1].email_permission, 'Domain')
        self.assertEqual(self.feed.entry[1].description, 'For try')


class GroupMemberEntryTest(unittest.TestCase):
    def setUp(self):
        self.entry = atom.core.parse(test_data.GROUP_MEMBER_ENTRY,
                                     gdata.apps.groups.data.GroupMemberEntry)
        self.feed = atom.core.parse(test_data.GROUP_MEMBER_FEED,
                                    gdata.apps.groups.data.GroupMemberFeed)

    def testGroupMemberEntryFromString(self):
        self.assertTrue(isinstance(self.entry,
                                   gdata.apps.groups.data.GroupMemberEntry))
        self.assertEqual(self.entry.member_id, 'abcd12310@srkapps.com')
        self.assertEqual(self.entry.member_type, 'User')
        self.assertEqual(self.entry.direct_member, 'true')

    def testGroupMemberFeedFromString(self):
        self.assertEqual(len(self.feed.entry), 2)
        self.assertTrue(isinstance(self.feed,
                                   gdata.apps.groups.data.GroupMemberFeed))
        self.assertTrue(isinstance(self.feed.entry[0],
                                   gdata.apps.groups.data.GroupMemberEntry))
        self.assertTrue(isinstance(self.feed.entry[1],
                                   gdata.apps.groups.data.GroupMemberEntry))
        self.assertEqual(
            self.feed.entry[0].find_edit_link(),
            ('http://apps-apis.google.com/a/feeds/group/2.0/srkapps.com/trial/'
             'member/abcd12310%40srkapps.com'))
        self.assertEqual(self.feed.entry[0].member_id, 'abcd12310@srkapps.com')
        self.assertEqual(self.feed.entry[0].member_type, 'User')
        self.assertEqual(self.feed.entry[0].direct_member, 'true')
        self.assertEqual(
            self.feed.entry[1].find_edit_link(),
            ('http://apps-apis.google.com/a/feeds/group/2.0/srkapps.com/trial/'
             'member/neha.technocrat%40srkapps.com'))
        self.assertEqual(self.feed.entry[1].member_id,
                         'neha.technocrat@srkapps.com')
        self.assertEqual(self.feed.entry[1].member_type, 'User')
        self.assertEqual(self.feed.entry[1].direct_member, 'true')


def suite():
    return conf.build_suite([GroupEntryTest, GroupMemberEntryTest])


if __name__ == '__main__':
    unittest.main()
