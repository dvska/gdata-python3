#!/usr/bin/env python
#
# Copyright (C) 2010 Google Inc.
#
# Licensed under the Apache License 2.0;


"""Unit Tests for Google Analytics API query objects.

AnalyticsClientTest: Tests making live requests to Google Analytics API.
"""

# __author__ = 'api.nickm@google.com (Nick Mihailovski)'

import unittest

from gdata.analytics import client


class DataExportQueryTest(unittest.TestCase):
    """Tests making Data Export API Queries."""

    def testAccountFeed(self):
        """Tests Account Feed queries."""
        queryTest1 = client.AccountFeedQuery()
        self.assertEqual(str(queryTest1),
                         'https://www.google.com/analytics/feeds/accounts/default')

        queryTest2 = client.AccountFeedQuery({'max-results': 50})
        self.assertEqual(str(queryTest2),
                         'https://www.google.com/analytics/feeds/accounts/default'
                         '?max-results=50')

        queryTest3 = client.AccountFeedQuery()
        queryTest3.query['max-results'] = 100
        self.assertEqual(str(queryTest3),
                         'https://www.google.com/analytics/feeds/accounts/default'
                         '?max-results=100')

    def testDataFeed(self):
        """Tests Data Feed queries."""
        queryTest1 = client.DataFeedQuery()
        self.assertEqual(str(queryTest1),
                         'https://www.google.com/analytics/feeds/data')

        queryTest2 = client.DataFeedQuery({'ids': 'ga:1234'})
        self.assertEqual(str(queryTest2),
                         'https://www.google.com/analytics/feeds/data?ids=ga%3A1234')

        queryTest3 = client.DataFeedQuery()
        queryTest3.query['ids'] = 'ga:1234'
        self.assertEqual(str(queryTest3),
                         'https://www.google.com/analytics/feeds/data?ids=ga%3A1234')


class ManagementQueryTest(unittest.TestCase):
    """Tests making Management API queries."""

    def setUp(self):
        self.base_url = 'https://www.google.com/analytics/feeds/datasources/ga'

    def testAccountFeedQuery(self):
        """Tests Account Feed queries."""
        queryTest1 = client.AccountQuery()
        self.assertEqual(str(queryTest1),
                         '%s/accounts' % self.base_url)

        queryTest2 = client.AccountQuery({'max-results': 50})
        self.assertEqual(str(queryTest2),
                         '%s/accounts?max-results=50' % self.base_url)

    def testWebPropertyFeedQuery(self):
        """Tests Web Property Feed queries."""
        queryTest1 = client.WebPropertyQuery()
        self.assertEqual(str(queryTest1),
                         '%s/accounts/~all/webproperties' % self.base_url)

        queryTest2 = client.WebPropertyQuery('123')
        self.assertEqual(str(queryTest2),
                         '%s/accounts/123/webproperties' % self.base_url)

        queryTest3 = client.WebPropertyQuery('123', {'max-results': 100})
        self.assertEqual(str(queryTest3),
                         '%s/accounts/123/webproperties?max-results=100' % self.base_url)

    def testProfileFeedQuery(self):
        """Tests Profile Feed queries."""
        queryTest1 = client.ProfileQuery()
        self.assertEqual(str(queryTest1),
                         '%s/accounts/~all/webproperties/~all/profiles' % self.base_url)

        queryTest2 = client.ProfileQuery('123', 'UA-123-1')
        self.assertEqual(str(queryTest2),
                         '%s/accounts/123/webproperties/UA-123-1/profiles' % self.base_url)

        queryTest3 = client.ProfileQuery('123', 'UA-123-1',
                                         {'max-results': 100})
        self.assertEqual(str(queryTest3),
                         '%s/accounts/123/webproperties/UA-123-1/profiles?max-results=100'
                         % self.base_url)

        queryTest4 = client.ProfileQuery()
        queryTest4.acct_id = '123'
        queryTest4.web_prop_id = 'UA-123-1'
        queryTest4.query['max-results'] = 100
        self.assertEqual(str(queryTest4),
                         '%s/accounts/123/webproperties/UA-123-1/profiles?max-results=100'
                         % self.base_url)

    def testGoalFeedQuery(self):
        """Tests Goal Feed queries."""
        queryTest1 = client.GoalQuery()
        self.assertEqual(str(queryTest1),
                         '%s/accounts/~all/webproperties/~all/profiles/~all/goals'
                         % self.base_url)

        queryTest2 = client.GoalQuery('123', 'UA-123-1', '555')
        self.assertEqual(str(queryTest2),
                         '%s/accounts/123/webproperties/UA-123-1/profiles/555/goals'
                         % self.base_url)

        queryTest3 = client.GoalQuery('123', 'UA-123-1', '555',
                                      {'max-results': 100})
        self.assertEqual(str(queryTest3),
                         '%s/accounts/123/webproperties/UA-123-1/profiles/555/goals'
                         '?max-results=100' % self.base_url)

        queryTest4 = client.GoalQuery()
        queryTest4.acct_id = '123'
        queryTest4.web_prop_id = 'UA-123-1'
        queryTest4.profile_id = '555'
        queryTest4.query['max-results'] = 100
        self.assertEqual(str(queryTest3),
                         '%s/accounts/123/webproperties/UA-123-1/profiles/555/goals'
                         '?max-results=100' % self.base_url)

    def testAdvSegQuery(self):
        """Tests Advanced Segment Feed queries."""
        queryTest1 = client.AdvSegQuery()
        self.assertEqual(str(queryTest1),
                         '%s/segments'
                         % self.base_url)

        queryTest2 = client.AdvSegQuery({'max-results': 100})
        self.assertEqual(str(queryTest2),
                         '%s/segments?max-results=100'
                         % self.base_url)


def suite():
    return conf.build_suite([DataExportQueryTest,
                             ManagementQueryTest])


if __name__ == '__main__':
    unittest.main()
