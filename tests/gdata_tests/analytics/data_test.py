#!/usr/bin/env python
#
# Copyright (C) 2010 Google Inc.
#
# Licensed under the Apache License 2.0;


"""Unit Tests for Google Analytics Data Export API and Management APIs.

Although the Data Export API and Management API conceptually operate on
different parts of Google Analytics, the APIs share some code so they
are released in the same module.

AccountFeedTest: All unit tests for AccountFeed class.
DataFeedTest: All unit tests for DataFeed class.
ManagementFeedAccountTest: Unit tests for ManagementFeed class.
ManagementFeedGoalTest: Unit tests for ManagementFeed class.
ManagementFeedAdvSegTest: Unit tests for ManagementFeed class.
"""

# __author__ = 'api.nickm@google.com (Nick Mihailovski)'

import unittest

import atom.core
import gdata.analytics.data
import gdata.test_config as conf
from gdata import test_data


class AccountFeedTest(unittest.TestCase):
    """Unit test for all custom elements in the Account Feed."""

    def setUp(self):
        """Retrieves the test XML feed into a AccountFeed object."""
        self.feed = atom.core.parse(test_data.ANALYTICS_ACCOUNT_FEED,
                                    gdata.analytics.data.AccountFeed)

    def testSegment(self):
        """Tests Segment class in Google Analytics Account Feed."""

        segment = self.feed.segment[0]
        self.assertEqual(segment.id, 'gaid::-11')
        self.assertEqual(segment.name, 'Visits from iPhones')

    def testSegmentDefinition(self):
        """Tests Definition class in Google Analytics Account Feed."""

        definition = self.feed.segment[0].definition
        self.assertEqual(definition.text, 'ga:operatingSystem==iPhone')

    def testEntryTableId(self):
        """Tests custom classes in Google Analytics Account Feed."""

        entry = self.feed.entry[0]
        self.assertEqual(entry.table_id.text, 'ga:1174')

    def testEntryProperty(self):
        """Tests the property classes in Google Analytics Account Feed."""
        property = self.feed.entry[0].property

        self.assertEqual(property[0].name, 'ga:accountId')
        self.assertEqual(property[0].value, '30481')

        self.assertEqual(property[1].name, 'ga:accountName')
        self.assertEqual(property[1].value, 'Google Store')

        self.assertEqual(property[2].name, 'ga:profileId')
        self.assertEqual(property[2].value, '1174')

        self.assertEqual(property[3].name, 'ga:webPropertyId')
        self.assertEqual(property[3].value, 'UA-30481-1')

        self.assertEqual(property[4].name, 'ga:currency')
        self.assertEqual(property[4].value, 'USD')

        self.assertEqual(property[5].name, 'ga:timezone')
        self.assertEqual(property[5].value, 'America/Los_Angeles')

    def testEntryGetProperty(self):
        """Tests GetProperty inherited class in the AccountEntry class."""

        entry = self.feed.entry[0]
        self.assertEqual(entry.GetProperty('ga:accountId').value, '30481')
        self.assertEqual(entry.GetProperty('ga:accountName').value, 'Google Store')
        self.assertEqual(entry.GetProperty('ga:profileId').value, '1174')
        self.assertEqual(entry.GetProperty('ga:webPropertyId').value, 'UA-30481-1')
        self.assertEqual(entry.GetProperty('ga:currency').value, 'USD')
        self.assertEqual(entry.GetProperty('ga:timezone').value, 'America/Los_Angeles')

    def testGoal(self):
        """Tests Goal class in Google Anlaytics Account Feed."""

        goal = self.feed.entry[0].goal[0]
        self.assertEqual(goal.number, '1')
        self.assertEqual(goal.name, 'Completing Order')
        self.assertEqual(goal.value, '10.0')
        self.assertEqual(goal.active, 'true')

    def testDestination(self):
        """Tests Destination class in Google Analytics Account Feed."""

        destination = self.feed.entry[0].goal[0].destination
        self.assertEqual(destination.expression, '/purchaseComplete.html')
        self.assertEqual(destination.case_sensitive, 'false')
        self.assertEqual(destination.match_type, 'regex')
        self.assertEqual(destination.step1_required, 'false')

    def testStep(self):
        """Tests Step class in Google Analytics Account Feed."""

        step = self.feed.entry[0].goal[0].destination.step[0]
        self.assertEqual(step.number, '1')
        self.assertEqual(step.name, 'View Product Categories')
        self.assertEqual(step.path, '/Apps|Accessories|Fun|Kid\+s|Office')

    def testEngagemet(self):
        """Tests Engagement class in Google Analytics Account Feed."""

        engagement = self.feed.entry[0].goal[1].engagement
        self.assertEqual(engagement.type, 'timeOnSite')
        self.assertEqual(engagement.comparison, '>')
        self.assertEqual(engagement.threshold_value, '300')

    def testCustomVariable(self):
        """Tests CustomVariable class in Google Analytics Account Feed."""

        customVar = self.feed.entry[0].custom_variable[0]
        self.assertEqual(customVar.index, '1')
        self.assertEqual(customVar.name, 'My Custom Variable')
        self.assertEqual(customVar.scope, '3')


class DataFeedTest(unittest.TestCase):
    """Unit test for all custom elements in the Data Feed."""

    def setUp(self):
        """Retrieves the test XML feed into a DataFeed object."""

        self.feed = atom.core.parse(test_data.ANALYTICS_DATA_FEED,
                                    gdata.analytics.data.DataFeed)

    def testDataFeed(self):
        """Tests custom classes in Google Analytics Data Feed."""

        self.assertEqual(self.feed.start_date.text, '2008-10-01')
        self.assertEqual(self.feed.end_date.text, '2008-10-31')

    def testAggregates(self):
        """Tests Aggregates class in Google Analytics Data Feed."""

        self.assertTrue(self.feed.aggregates is not None)

    def testContainsSampledData(self):
        """Tests ContainsSampledData class in Google Analytics Data Feed."""

        contains_sampled_data = self.feed.contains_sampled_data.text
        self.assertEqual(contains_sampled_data, 'true')
        self.assertTrue(self.feed.HasSampledData())

    def testAggregatesElements(self):
        """Tests Metrics class in Aggregates class."""

        metric = self.feed.aggregates.metric[0]
        self.assertEqual(metric.confidence_interval, '0.0')
        self.assertEqual(metric.name, 'ga:visits')
        self.assertEqual(metric.type, 'integer')
        self.assertEqual(metric.value, '136540')

        metric = self.feed.aggregates.GetMetric('ga:visits')
        self.assertEqual(metric.confidence_interval, '0.0')
        self.assertEqual(metric.name, 'ga:visits')
        self.assertEqual(metric.type, 'integer')
        self.assertEqual(metric.value, '136540')

    def testDataSource(self):
        """Tests DataSources class in Google Analytics Data Feed."""

        self.assertTrue(self.feed.data_source[0] is not None)

    def testDataSourceTableId(self):
        """Tests TableId class in the DataSource class."""

        table_id = self.feed.data_source[0].table_id
        self.assertEqual(table_id.text, 'ga:1174')

    def testDataSourceTableName(self):
        """Tests TableName class in the DataSource class."""

        table_name = self.feed.data_source[0].table_name
        self.assertEqual(table_name.text, 'www.googlestore.com')

    def testDataSourceProperty(self):
        """Tests Property class in the DataSource class."""

        property = self.feed.data_source[0].property
        self.assertEqual(property[0].name, 'ga:profileId')
        self.assertEqual(property[0].value, '1174')

        self.assertEqual(property[1].name, 'ga:webPropertyId')
        self.assertEqual(property[1].value, 'UA-30481-1')

        self.assertEqual(property[2].name, 'ga:accountName')
        self.assertEqual(property[2].value, 'Google Store')

    def testDataSourceGetProperty(self):
        """Tests GetProperty utility method in the DataSource class."""

        ds = self.feed.data_source[0]
        self.assertEqual(ds.GetProperty('ga:profileId').value, '1174')
        self.assertEqual(ds.GetProperty('ga:webPropertyId').value, 'UA-30481-1')
        self.assertEqual(ds.GetProperty('ga:accountName').value, 'Google Store')

    def testSegment(self):
        """Tests Segment class in DataFeed class."""

        segment = self.feed.segment
        self.assertEqual(segment.id, 'gaid::-11')
        self.assertEqual(segment.name, 'Visits from iPhones')

    def testSegmentDefinition(self):
        """Tests Definition class in Segment class."""

        definition = self.feed.segment.definition
        self.assertEqual(definition.text, 'ga:operatingSystem==iPhone')

    def testEntryDimension(self):
        """Tests Dimension class in Entry class."""

        dim = self.feed.entry[0].dimension[0]
        self.assertEqual(dim.name, 'ga:source')
        self.assertEqual(dim.value, 'blogger.com')

    def testEntryGetDimension(self):
        """Tests GetDimension utility method in the Entry class."""

        dim = self.feed.entry[0].GetDimension('ga:source')
        self.assertEqual(dim.name, 'ga:source')
        self.assertEqual(dim.value, 'blogger.com')

        error = self.feed.entry[0].GetDimension('foo')
        self.assertEqual(error, None)

    def testEntryMetric(self):
        """Tests Metric class in Entry class."""

        met = self.feed.entry[0].metric[0]
        self.assertEqual(met.confidence_interval, '0.0')
        self.assertEqual(met.name, 'ga:visits')
        self.assertEqual(met.type, 'integer')
        self.assertEqual(met.value, '68140')

    def testEntryGetMetric(self):
        """Tests GetMetric utility method in the Entry class."""

        met = self.feed.entry[0].GetMetric('ga:visits')
        self.assertEqual(met.confidence_interval, '0.0')
        self.assertEqual(met.name, 'ga:visits')
        self.assertEqual(met.type, 'integer')
        self.assertEqual(met.value, '68140')

        error = self.feed.entry[0].GetMetric('foo')
        self.assertEqual(error, None)

    def testEntryGetObject(self):
        """Tests GetObjectOf utility method in Entry class."""

        entry = self.feed.entry[0]

        dimension = entry.GetObject('ga:source')
        self.assertEqual(dimension.name, 'ga:source')
        self.assertEqual(dimension.value, 'blogger.com')

        metric = entry.GetObject('ga:visits')
        self.assertEqual(metric.name, 'ga:visits')
        self.assertEqual(metric.value, '68140')
        self.assertEqual(metric.type, 'integer')
        self.assertEqual(metric.confidence_interval, '0.0')

        error = entry.GetObject('foo')
        self.assertEqual(error, None)


class ManagementFeedProfileTest(unittest.TestCase):
    """Unit test for all property elements in Google Analytics Management Feed.

    Since the Account, Web Property and Profile feed all have the same
    structure and XML elements, this single test case covers all three feeds.
    """

    def setUp(self):
        """Retrieves the test XML feed into a DataFeed object."""

        self.feed = atom.core.parse(test_data.ANALYTICS_MGMT_PROFILE_FEED,
                                    gdata.analytics.data.ManagementFeed)

    def testFeedKindAttribute(self):
        """Tests the kind attribute in the feed."""

        self.assertEqual(self.feed.kind, 'analytics#profiles')

    def testEntryKindAttribute(self):
        """tests the kind attribute in the entry."""

        entry_kind = self.feed.entry[0].kind
        self.assertEqual(entry_kind, 'analytics#profile')

    def testEntryProperty(self):
        """Tests property classes in Managment Entry class."""

        property = self.feed.entry[0].property
        self.assertEqual(property[0].name, 'ga:accountId')
        self.assertEqual(property[0].value, '30481')

    def testEntryGetProperty(self):
        """Tests GetProperty helper method in Management Entry class."""

        entry = self.feed.entry[0]
        self.assertEqual(entry.GetProperty('ga:accountId').value, '30481')

    def testGetParentLinks(self):
        """Tests GetParentLinks utility method."""

        parent_links = self.feed.entry[0].GetParentLinks()
        self.assertEqual(len(parent_links), 1)

        parent_link = parent_links[0]
        self.assertEqual(parent_link.rel,
                         'http://schemas.google.com/ga/2009#parent')
        self.assertEqual(parent_link.type,
                         'application/atom+xml')
        self.assertEqual(parent_link.href,
                         'https://www.google.com/analytics/feeds/datasources'
                         '/ga/accounts/30481/webproperties/UA-30481-1')
        self.assertEqual(parent_link.target_kind,
                         'analytics#webproperty')

    def testGetChildLinks(self):
        """Tests GetChildLinks utility method."""

        child_links = self.feed.entry[0].GetChildLinks()
        self.assertEqual(len(child_links), 1)

        self.ChildLinkTestHelper(child_links[0])

    def testGetChildLink(self):
        """Tests getChildLink utility method."""

        child_link = self.feed.entry[0].GetChildLink('analytics#goals')
        self.ChildLinkTestHelper(child_link)

        child_link = self.feed.entry[0].GetChildLink('foo_bar')
        self.assertEqual(child_link, None)

    def ChildLinkTestHelper(self, child_link):
        """Common method to test a child link."""

        self.assertEqual(child_link.rel,
                         'http://schemas.google.com/ga/2009#child')
        self.assertEqual(child_link.type,
                         'application/atom+xml')
        self.assertEqual(child_link.href,
                         'https://www.google.com/analytics/feeds/datasources'
                         '/ga/accounts/30481/webproperties/UA-30481-1/profiles/1174/goals')
        self.assertEqual(child_link.target_kind,
                         'analytics#goals')


class ManagementFeedGoalTest(unittest.TestCase):
    """Unit test for all Goal elements in Management Feed."""

    def setUp(self):
        """Retrieves the test XML feed into a DataFeed object."""

        self.feed = atom.core.parse(test_data.ANALYTICS_MGMT_GOAL_FEED,
                                    gdata.analytics.data.ManagementFeed)

    def testEntryGoal(self):
        """Tests Goal class in Google Anlaytics Account Feed."""

        goal = self.feed.entry[0].goal
        self.assertEqual(goal.number, '1')
        self.assertEqual(goal.name, 'Completing Order')
        self.assertEqual(goal.value, '10.0')
        self.assertEqual(goal.active, 'true')

    def testGoalDestination(self):
        """Tests Destination class in Google Analytics Account Feed."""

        destination = self.feed.entry[0].goal.destination
        self.assertEqual(destination.expression, '/purchaseComplete.html')
        self.assertEqual(destination.case_sensitive, 'false')
        self.assertEqual(destination.match_type, 'regex')
        self.assertEqual(destination.step1_required, 'false')

    def testGoalDestinationStep(self):
        """Tests Step class in Google Analytics Account Feed."""

        step = self.feed.entry[0].goal.destination.step[0]
        self.assertEqual(step.number, '1')
        self.assertEqual(step.name, 'View Product Categories')
        self.assertEqual(step.path, '/Apps|Accessories')

    def testGoalEngagemet(self):
        """Tests Engagement class in Google Analytics Account Feed."""

        engagement = self.feed.entry[1].goal.engagement
        self.assertEqual(engagement.type, 'timeOnSite')
        self.assertEqual(engagement.comparison, '>')
        self.assertEqual(engagement.threshold_value, '300')


class ManagementFeedAdvSegTest(unittest.TestCase):
    """Unit test for all Advanced Segment elements in Management Feed."""

    def setUp(self):
        """Retrieves the test XML feed into a DataFeed object."""

        self.feed = atom.core.parse(test_data.ANALYTICS_MGMT_ADV_SEGMENT_FEED,
                                    gdata.analytics.data.ManagementFeed)

    def testEntrySegment(self):
        """Tests Segment class in ManagementEntry class."""

        segment = self.feed.entry[0].segment
        self.assertEqual(segment.id, 'gaid::0')
        self.assertEqual(segment.name, 'Sources Form Google')

    def testSegmentDefinition(self):
        """Tests Definition class in Segment class."""

        definition = self.feed.entry[0].segment.definition
        self.assertEqual(definition.text, 'ga:source=~^\Qgoogle\E')


def suite():
    """Test Account Feed, Data Feed and Management API Feeds."""
    return conf.build_suite([
        AccountFeedTest,
        DataFeedTest,
        ManagementFeedProfileTest,
        ManagementFeedGoalTest,
        ManagementFeedAdvSegTest])


if __name__ == '__main__':
    unittest.main()
