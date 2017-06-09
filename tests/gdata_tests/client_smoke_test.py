#!/usr/bin/env python
#
# Copyright (C) 2010 Google Inc.
#
# Licensed under the Apache License 2.0;



# This module is used for version 2 of the Google Data APIs.


# __author__ = 'j.s@google.com (Jeff Scudder)'

import unittest

import gdata.analytics.client
import gdata.apps.emailsettings.client
import gdata.blogger.client
import gdata.calendar_resource.client
import gdata.contacts.client
import gdata.docs.client
import gdata.projecthosting.client
import gdata.sites.client
import gdata.spreadsheets.client
import gdata.test_config as conf


class ClientSmokeTest(unittest.TestCase):
    def test_check_auth_client_classes(self):
        conf.check_clients_with_auth(self, (
            gdata.analytics.client.AnalyticsClient,
            gdata.apps.emailsettings.client.EmailSettingsClient,
            gdata.blogger.client.BloggerClient,
            gdata.spreadsheets.client.SpreadsheetsClient,
            gdata.calendar_resource.client.CalendarResourceClient,
            gdata.contacts.client.ContactsClient,
            gdata.docs.client.DocsClient,
            gdata.projecthosting.client.ProjectHostingClient,
            gdata.sites.client.SitesClient
        ))


def suite():
    return conf.build_suite([ClientSmokeTest])


if __name__ == '__main__':
    unittest.main()
