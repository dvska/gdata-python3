#!/usr/bin/env python
#
# Copyright (C) 2009 Google Inc.
#
# Licensed under the Apache License 2.0;


# This module is used for version 2 of the Google Data APIs.

# __author__ = 'jlapenna@google.com (Joe LaPenna)'

import unittest

import atom.core
import gdata.projecthosting.data
import gdata.test_config as conf

ISSUE_ENTRY = """\
<entry xmlns='http://www.w3.org/2005/Atom'
        xmlns:issues='http://schemas.google.com/projecthosting/issues/2009'>
  <id>http://code.google.com/feeds/issues/p/PROJECT_NAME/issues/full/1</id>
  <updated>2009-09-09T20:34:35.365Z</updated>
  <title>This is updated issue summary</title>
  <content type='html'>This is issue description</content>
  <link rel='self' type='application/atom+xml'
      href='http://code.google.com/feeds/issues/p/PROJECT_NAME/issues/full/3'/>
  <link rel='edit' type='application/atom+xml'
      href='http://code.google.com/feeds/issues/p/PROJECT_NAME/issues/full/3'/>
  <author>
    <name>elizabeth.bennet</name>
    <uri>/u/elizabeth.bennet/</uri>
  </author>
  <issues:cc>
    <issues:uri>/u/@UBhTQl1UARRAVga7/</issues:uri>
    <issues:username>mar...@domain.com</issues:username>
  </issues:cc>
  <issues:cc>
    <issues:uri>/u/fitzwilliam.darcy/</issues:uri>
    <issues:username>fitzwilliam.darcy</issues:username>
  </issues:cc>
  <issues:label>Type-Enhancement</issues:label>
  <issues:label>Priority-Low</issues:label>
  <issues:owner>
    <issues:uri>/u/charlotte.lucas/</issues:uri>
    <issues:username>charlotte.lucas</issues:username>
  </issues:owner>
  <issues:stars>0</issues:stars>
  <issues:state>open</issues:state>
  <issues:status>Started</issues:status>
</entry>
"""

ISSUES_FEED = """\
<?xml version='1.0' encoding='UTF-8'?>
<feed xmlns='http://www.w3.org/2005/Atom'>
  <id>http://code.google.com/feeds/issues/p/android-test2/issues/full</id>
  <link href="http://code.google.com/feeds/issues/p/android-test2/issues/full"
      rel="http://schemas.google.com/g/2005#feed" type="application/atom+xml" />
  <link href="http://code.google.com/feeds/issues/p/android-test2/issues/full"
      rel="http://schemas.google.com/g/2005#post" type="application/atom+xml" />
  <link href="http://code.google.com/feeds/issues/p/android-test2/issues/full"
      rel="self" type="application/atom+xml" />
  <updated>2009-09-22T04:06:32.794Z</updated>
  %s
</feed>
""" % ISSUE_ENTRY

COMMENT_ENTRY = """\
<?xml version='1.0' encoding='UTF-8'?>
<entry xmlns='http://www.w3.org/2005/Atom'
    xmlns:issues='http://schemas.google.com/projecthosting/issues/2009'>
  <content type='html'>This is comment - update issue</content>
  <author>
    <name>elizabeth.bennet</name>
  </author>
  <issues:updates>
    <issues:summary>This is updated issue summary</issues:summary>
    <issues:status>Started</issues:status>
    <issues:ownerUpdate>charlotte.lucas</issues:ownerUpdate>
    <issues:label>-Type-Defect</issues:label>
    <issues:label>Type-Enhancement</issues:label>
    <issues:label>-Milestone-2009</issues:label>
    <issues:label>-Priority-Medium</issues:label>
    <issues:label>Priority-Low</issues:label>
    <issues:ccUpdate>-fitzwilliam.darcy</issues:ccUpdate>
    <issues:ccUpdate>marialucas@domain.com</issues:ccUpdate>
  </issues:updates>
</entry>
"""


class CommentEntryTest(unittest.TestCase):
    def testParsing(self):
        entry = atom.core.parse(COMMENT_ENTRY,
                                gdata.projecthosting.data.CommentEntry)

        updates = entry.updates

        self.assertEqual(updates.summary.text, 'This is updated issue summary')
        self.assertEqual(updates.status.text, 'Started')
        self.assertEqual(updates.ownerUpdate.text, 'charlotte.lucas')

        self.assertEqual(len(updates.label), 5)
        self.assertEqual(updates.label[0].text, '-Type-Defect')
        self.assertEqual(updates.label[1].text, 'Type-Enhancement')
        self.assertEqual(updates.label[2].text, '-Milestone-2009')
        self.assertEqual(updates.label[3].text, '-Priority-Medium')
        self.assertEqual(updates.label[4].text, 'Priority-Low')

        self.assertEqual(len(updates.ccUpdate), 2)
        self.assertEqual(updates.ccUpdate[0].text, '-fitzwilliam.darcy')
        self.assertEqual(updates.ccUpdate[1].text, 'marialucas@domain.com')


class IssueEntryTest(unittest.TestCase):
    def testParsing(self):
        entry = atom.core.parse(ISSUE_ENTRY, gdata.projecthosting.data.IssueEntry)

        self.assertEqual(entry.owner.uri.text, '/u/charlotte.lucas/')
        self.assertEqual(entry.owner.username.text, 'charlotte.lucas')

        self.assertEqual(len(entry.cc), 2)
        cc_0 = entry.cc[0]
        self.assertEqual(cc_0.uri.text, '/u/@UBhTQl1UARRAVga7/')
        self.assertEqual(cc_0.username.text, 'mar...@domain.com')
        cc_1 = entry.cc[1]
        self.assertEqual(cc_1.uri.text, '/u/fitzwilliam.darcy/')
        self.assertEqual(cc_1.username.text, 'fitzwilliam.darcy')

        self.assertEqual(len(entry.label), 2)
        self.assertEqual(entry.label[0].text, 'Type-Enhancement')
        self.assertEqual(entry.label[1].text, 'Priority-Low')

        self.assertEqual(entry.stars.text, '0')
        self.assertEqual(entry.state.text, 'open')
        self.assertEqual(entry.status.text, 'Started')


class DataClassSanityTest(unittest.TestCase):
    def test_basic_element_structure(self):
        conf.check_data_classes(self, [
            gdata.projecthosting.data.Uri,
            gdata.projecthosting.data.Username,
            gdata.projecthosting.data.Cc,
            gdata.projecthosting.data.Label,
            gdata.projecthosting.data.Owner,
            gdata.projecthosting.data.Stars,
            gdata.projecthosting.data.State,
            gdata.projecthosting.data.Status,
            gdata.projecthosting.data.Summary,
            gdata.projecthosting.data.Updates,
            gdata.projecthosting.data.IssueEntry,
            gdata.projecthosting.data.IssuesFeed,
            gdata.projecthosting.data.CommentEntry,
            gdata.projecthosting.data.CommentsFeed])


def suite():
    return conf.build_suite([IssueEntryTest, DataClassSanityTest])


if __name__ == '__main__':
    unittest.main()
