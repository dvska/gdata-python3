#
# Copyright 2008 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License 2.0;


"""Test for Email Migration service."""

# __author__ = 'google-apps-apis@googlegroups.com'

import getpass
import unittest

import gdata.apps.migration.service

domain = ''
admin_email = ''
admin_password = ''
username = ''
MESSAGE = """From: joe@blow.com
To: jane@doe.com
Date: Mon, 29 Sep 2008 20:00:34 -0500 (CDT)
Subject: %s

%s"""


class MigrationTest(unittest.TestCase):
    """Test for the MigrationService."""

    def setUp(self):
        self.ms = gdata.apps.migration.service.MigrationService(
            email=admin_email, password=admin_password, domain=domain)
        self.ms.ProgrammaticLogin()

    def testImportMail(self):
        self.ms.ImportMail(user_name=username,
                           mail_message=MESSAGE % ('Test subject', 'Test body'),
                           mail_item_properties=['IS_STARRED'],
                           mail_labels=['Test'])

    def testImportMultipleMails(self):
        for i in range(1, 10):
            self.ms.AddMailEntry(mail_message=MESSAGE % ('Test thread %d' % i,
                                                         'Test thread'),
                                 mail_item_properties=['IS_UNREAD'],
                                 mail_labels=['Test', 'Thread'],
                                 identifier=str(i))
        self.ms.ImportMultipleMails(user_name=username)


if __name__ == '__main__':
    print("Google Apps Email Migration Service Tests\n\n"
          "NOTE: Please run these tests only with a test user account.\n")
    domain = input('Google Apps domain: ')
    admin_email = '%s@%s' % (input('Administrator username: '), domain)
    admin_password = getpass.getpass('Administrator password: ')
    username = input('Test username: ')
    unittest.main()
