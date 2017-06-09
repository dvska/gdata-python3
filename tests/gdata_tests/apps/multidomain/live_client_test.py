#
# Copyright 2011 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License 2.0;


"""Live client tests for the Multidomain Provisioning API."""

# This module is used for version 2 of the Google Data APIs.
# These tests attempt to connect to Google servers.


# __author__ = 'Claudio Cherubino <ccherubino@google.com>'

import random
import unittest

import gdata.apps.multidomain.client
import gdata.apps.multidomain.data
import gdata.client
import gdata.data
import gdata.gauth
import gdata.test_config as conf

conf.options.register_option(conf.APPS_DOMAIN_OPTION)


class MultidomainProvisioningClientTest(unittest.TestCase):
    def setUp(self):
        self.client = gdata.apps.multidomain.client.MultiDomainProvisioningClient(
            domain='example.com')
        if conf.options.get_value('runlive') == 'true':
            self.client = gdata.apps.multidomain.client.MultiDomainProvisioningClient(
                domain=conf.options.get_value('appsdomain'))
            if conf.options.get_value('ssl') == 'true':
                self.client.ssl = True
            conf.configure_client(self.client, 'MultidomainProvisioningClientTest',
                                  self.client.auth_service, True)

    def tearDown(self):
        conf.close_client(self.client)

    def testClientConfiguration(self):
        self.assertEqual('apps-apis.google.com', self.client.host)
        self.assertEqual('2.0', self.client.api_version)
        self.assertEqual('apps', self.client.auth_service)
        self.assertEqual(gdata.gauth.AUTH_SCOPES['apps'], self.client.auth_scopes)
        if conf.options.get_value('runlive') == 'true':
            self.assertEqual(self.client.domain, conf.options.get_value('appsdomain'))
        else:
            self.assertEqual(self.client.domain, 'example.com')

    def testMakeMultidomainUserProvisioningUri(self):
        self.assertEqual('/a/feeds/user/2.0/%s' % self.client.domain,
                         self.client.MakeMultidomainUserProvisioningUri())
        self.assertEqual('/a/feeds/user/2.0/%s/liz@example.com'
                         % self.client.domain,
                         self.client.MakeMultidomainUserProvisioningUri(
                             email='liz@example.com'))
        self.assertEqual('/a/feeds/user/2.0/%s?start=%s'
                         % (self.client.domain, 'liz%40example.com'),
                         self.client.MakeMultidomainUserProvisioningUri(
                             params={'start': 'liz@example.com'}))

    def testMakeMultidomainAliasProvisioningUri(self):
        self.assertEqual('/a/feeds/alias/2.0/%s' % self.client.domain,
                         self.client.MakeMultidomainAliasProvisioningUri())
        self.assertEqual('/a/feeds/alias/2.0/%s/liz@example.com'
                         % self.client.domain,
                         self.client.MakeMultidomainAliasProvisioningUri(
                             email='liz@example.com'))
        self.assertEqual('/a/feeds/alias/2.0/%s?start=%s'
                         % (self.client.domain, 'liz%40example.com'),
                         self.client.MakeMultidomainAliasProvisioningUri(
                             params={'start': 'liz@example.com'}))

    def testCreateRetrieveUpdateDelete(self):
        if not conf.options.get_value('runlive') == 'true':
            return

        # Either load the recording or prepare to make a live request.
        conf.configure_cache(self.client, 'testCreateUpdateDelete')

        rnd_number = random.randrange(0, 100001)
        email = 'test_user%s@%s' % (rnd_number, self.client.domain)
        alias = 'test_alias%s@%s' % (rnd_number, self.client.domain)

        new_entry = self.client.CreateUser(
            email, 'Elizabeth', 'Smith',
            '51eea05d46317fadd5cad6787a8f562be90b4446', 'true',
            hash_function='SHA-1')

        self.assertTrue(isinstance(new_entry,
                                   gdata.apps.multidomain.data.UserEntry))
        self.assertEqual(new_entry.first_name, 'Elizabeth')
        self.assertEqual(new_entry.last_name, 'Smith')
        self.assertEqual(new_entry.email, email)
        self.assertEqual(new_entry.password,
                         '51eea05d46317fadd5cad6787a8f562be90b4446')
        self.assertEqual(new_entry.is_admin, 'true')

        fetched_entry = self.client.RetrieveUser(email=email)
        self.assertEqual(fetched_entry.first_name, 'Elizabeth')
        self.assertEqual(fetched_entry.last_name, 'Smith')
        self.assertEqual(fetched_entry.email, email)
        self.assertEqual(fetched_entry.is_admin, 'true')

        new_entry.first_name = 'Joe'
        new_entry.last_name = 'Brown'
        updated_entry = self.client.UpdateUser(
            email=email, user_entry=new_entry)
        self.assertTrue(isinstance(updated_entry,
                                   gdata.apps.multidomain.data.UserEntry))
        self.assertEqual(updated_entry.first_name, 'Joe')
        self.assertEqual(updated_entry.last_name, 'Brown')

        new_email = 'renamed_user%s@%s' % (rnd_number, self.client.domain)
        renamed_entry = self.client.RenameUser(
            old_email=email, new_email=new_email)
        self.assertTrue(isinstance(renamed_entry,
                                   gdata.apps.multidomain.data.UserRenameRequest))
        self.assertEqual(renamed_entry.new_email, new_email)

        new_alias = self.client.CreateAlias(new_email, alias)
        self.assertTrue(isinstance(new_alias,
                                   gdata.apps.multidomain.data.AliasEntry))
        self.assertEqual(new_alias.user_email, new_email)
        self.assertEqual(new_alias.alias_email, alias)

        fetched_alias = self.client.RetrieveAlias(alias)
        self.assertEqual(fetched_alias.user_email, new_email)
        self.assertEqual(fetched_alias.alias_email, alias)

        fetched_aliases = self.client.RetrieveAllUserAliases(new_email)
        self.assertEqual(fetched_aliases.entry[0].user_email, new_email)
        self.assertEqual(fetched_aliases.entry[0].alias_email, email)
        self.assertEqual(fetched_aliases.entry[1].user_email, new_email)
        self.assertEqual(fetched_aliases.entry[1].alias_email, alias)

        self.client.DeleteAlias(alias)
        self.client.DeleteUser(new_email)


def suite():
    return conf.build_suite([MultidomainProvisioningClientTest])


if __name__ == '__main__':
    unittest.TextTestRunner().run(suite())
