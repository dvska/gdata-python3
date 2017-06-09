#
# Copyright (C) 2007 Google Inc.
#
# Licensed under the Apache License 2.0;


# __author__ = 'api.jscudder (Jeff Scudder)'

import re
import unittest
import urllib.error
import urllib.parse
import urllib.request

import atom
import gdata.contacts.service
import gdata.test_config as conf

conf.options.register_option(conf.TEST_IMAGE_LOCATION_OPTION)


class ContactsServiceTest(unittest.TestCase):
    def setUp(self):
        self.gd_client = gdata.contacts.service.ContactsService()
        conf.configure_service(self.gd_client, 'ContactsServiceTest', 'cp')
        self.gd_client.email = conf.options.get_value('username')

    def tearDown(self):
        conf.close_service(self.gd_client)

    def testGetContactsFeed(self):
        if not conf.options.get_value('runlive') == 'true':
            return
        conf.configure_service_cache(self.gd_client, 'testGetContactsFeed')
        feed = self.gd_client.GetContactsFeed()
        self.assertTrue(isinstance(feed, gdata.contacts.ContactsFeed))

    def testDefaultContactList(self):
        self.assertEqual('default', self.gd_client.contact_list)

    def testCustomContactList(self):
        if not conf.options.get_value('runlive') == 'true':
            return
        conf.configure_service_cache(self.gd_client, 'testCustomContactList')

        self.gd_client.contact_list = conf.options.get_value('username')
        feed = self.gd_client.GetContactsFeed()
        self.assertTrue(isinstance(feed, gdata.contacts.ContactsFeed))

    def testGetFeedUriDefault(self):
        self.gd_client.contact_list = 'domain.com'
        self.assertEqual('/m8/feeds/contacts/domain.com/full',
                         self.gd_client.GetFeedUri())

    def testGetFeedUriCustom(self):
        uri = self.gd_client.GetFeedUri(kind='groups',
                                        contact_list='example.com',
                                        projection='base/batch',
                                        scheme='https')
        self.assertEqual(
            'https://www.google.com/m8/feeds/groups/example.com/base/batch', uri)

    def testCreateUpdateDeleteContactAndUpdatePhoto(self):
        if not conf.options.get_value('runlive') == 'true':
            return
        conf.configure_service_cache(self.gd_client, 'testCreateUpdateDeleteContactAndUpdatePhoto')

        DeleteTestContact(self.gd_client)

        # Create a new entry
        new_entry = gdata.contacts.ContactEntry()
        new_entry.title = atom.Title(text='Elizabeth Bennet')
        new_entry.content = atom.Content(text='Test Notes')
        new_entry.email.append(gdata.contacts.Email(
            rel='http://schemas.google.com/g/2005#work',
            primary='true',
            address='liz@gmail.com'))
        new_entry.phone_number.append(gdata.contacts.PhoneNumber(
            rel='http://schemas.google.com/g/2005#work', text='(206)555-1212'))
        new_entry.organization = gdata.contacts.Organization(
            org_name=gdata.contacts.OrgName(text='TestCo.'),
            rel='http://schemas.google.com/g/2005#work')

        entry = self.gd_client.CreateContact(new_entry)

        # Generate and parse the XML for the new entry.
        self.assertEqual(entry.title.text, new_entry.title.text)
        self.assertEqual(entry.content.text, 'Test Notes')
        self.assertEqual(len(entry.email), 1)
        self.assertEqual(entry.email[0].rel, new_entry.email[0].rel)
        self.assertEqual(entry.email[0].address, 'liz@gmail.com')
        self.assertEqual(len(entry.phone_number), 1)
        self.assertEqual(entry.phone_number[0].rel,
                         new_entry.phone_number[0].rel)
        self.assertEqual(entry.phone_number[0].text, '(206)555-1212')
        self.assertEqual(entry.organization.org_name.text, 'TestCo.')

        # Edit the entry.
        entry.phone_number[0].text = '(555)555-1212'
        updated = self.gd_client.UpdateContact(entry.GetEditLink().href, entry)
        self.assertEqual(updated.content.text, 'Test Notes')
        self.assertEqual(len(updated.phone_number), 1)
        self.assertEqual(updated.phone_number[0].rel,
                         entry.phone_number[0].rel)
        self.assertEqual(updated.phone_number[0].text, '(555)555-1212')

        # Change the contact's photo.
        updated_photo = self.gd_client.ChangePhoto(
            conf.options.get_value('imgpath'), updated,
            content_type='image/jpeg')

        # Refetch the contact so that it has the new photo link
        updated = self.gd_client.GetContact(updated.GetSelfLink().href)
        self.assertTrue(updated.GetPhotoLink() is not None)

        # Fetch the photo data.
        hosted_image = self.gd_client.GetPhoto(updated)
        self.assertTrue(hosted_image is not None)

        # Delete the entry.
        self.gd_client.DeleteContact(updated.GetEditLink().href)

    def testCreateAndDeleteContactUsingBatch(self):
        if not conf.options.get_value('runlive') == 'true':
            return
        conf.configure_service_cache(self.gd_client, 'testCreateAndDeleteContactUsingBatch')

        # Get random data for creating contact
        random_contact_number = 'notRandom12'
        random_contact_title = 'Random Contact %s' % (
            random_contact_number)

        # Set contact data
        contact = gdata.contacts.ContactEntry()
        contact.title = atom.Title(text=random_contact_title)
        contact.email = gdata.contacts.Email(
            address='user%s@example.com' % random_contact_number,
            primary='true',
            rel=gdata.contacts.REL_WORK)
        contact.content = atom.Content(text='Contact created by '
                                            'gdata-python-client automated test '
                                            'suite.')

        # Form a batch request
        batch_request = gdata.contacts.ContactsFeed()
        batch_request.AddInsert(entry=contact)

        # Execute the batch request to insert the contact.
        default_batch_url = gdata.contacts.service.DEFAULT_BATCH_URL
        batch_result = self.gd_client.ExecuteBatch(batch_request,
                                                   default_batch_url)

        self.assertEqual(len(batch_result.entry), 1)
        self.assertEqual(batch_result.entry[0].title.text,
                         random_contact_title)
        self.assertEqual(batch_result.entry[0].batch_operation.type,
                         gdata.BATCH_INSERT)
        self.assertEqual(batch_result.entry[0].batch_status.code,
                         '201')
        expected_batch_url = re.compile('default').sub(
            urllib.parse.quote(self.gd_client.email),
            gdata.contacts.service.DEFAULT_BATCH_URL)
        self.assertTrue(batch_result.GetBatchLink().href,
                        expected_batch_url)

        # Create a batch request to delete the newly created entry.
        batch_delete_request = gdata.contacts.ContactsFeed()
        batch_delete_request.AddDelete(entry=batch_result.entry[0])

        batch_delete_result = self.gd_client.ExecuteBatch(
            batch_delete_request,
            batch_result.GetBatchLink().href)
        self.assertEqual(len(batch_delete_result.entry), 1)
        self.assertEqual(batch_delete_result.entry[0].batch_operation.type,
                         gdata.BATCH_DELETE)
        self.assertEqual(batch_result.entry[0].batch_status.code,
                         '201')

    def testCleanUriNeedsCleaning(self):
        self.assertEqual('/relative/uri', self.gd_client._CleanUri(
            'http://www.google.com/relative/uri'))

    def testCleanUriDoesNotNeedCleaning(self):
        self.assertEqual('/relative/uri', self.gd_client._CleanUri(
            '/relative/uri'))


class ContactsQueryTest(unittest.TestCase):
    def testConvertToStringDefaultFeed(self):
        query = gdata.contacts.service.ContactsQuery()
        self.assertEqual(str(query), '/m8/feeds/contacts/default/full')
        query.max_results = 10
        self.assertEqual(query.ToUri(),
                         '/m8/feeds/contacts/default/full?max-results=10')

    def testConvertToStringCustomFeed(self):
        query = gdata.contacts.service.ContactsQuery('/custom/feed/uri')
        self.assertEqual(str(query), '/custom/feed/uri')
        query.max_results = '10'
        self.assertEqual(query.ToUri(), '/custom/feed/uri?max-results=10')

    def testGroupQueryParameter(self):
        query = gdata.contacts.service.ContactsQuery()
        query.group = 'http://google.com/m8/feeds/groups/liz%40gmail.com/full/270f'
        self.assertEqual(query.ToUri(), '/m8/feeds/contacts/default/full'
                                        '?group=http%3A%2F%2Fgoogle.com%2Fm8%2Ffeeds%2Fgroups'
                                        '%2Fliz%2540gmail.com%2Ffull%2F270f')


class ContactsGroupsTest(unittest.TestCase):
    def setUp(self):
        self.gd_client = gdata.contacts.service.ContactsService()
        conf.configure_service(self.gd_client, 'ContactsServiceTest', 'cp')

    def tearDown(self):
        conf.close_service(self.gd_client)

    def testCreateUpdateDeleteGroup(self):
        if not conf.options.get_value('runlive') == 'true':
            return
        conf.configure_service_cache(self.gd_client,
                                     'testCreateUpdateDeleteGroup')

        test_group = gdata.contacts.GroupEntry(title=atom.Title(
            text='test group py'))
        new_group = self.gd_client.CreateGroup(test_group)
        self.assertTrue(isinstance(new_group, gdata.contacts.GroupEntry))
        self.assertEqual(new_group.title.text, 'test group py')

        # Change the group's title
        new_group.title.text = 'new group name py'
        updated_group = self.gd_client.UpdateGroup(new_group.GetEditLink().href,
                                                   new_group)
        self.assertEqual(updated_group.title.text, new_group.title.text)

        # Remove the group
        self.gd_client.DeleteGroup(updated_group.GetEditLink().href)


# Utility methods.
def DeleteTestContact(client):
    # Get test contact
    feed = client.GetContactsFeed()
    for entry in feed.entry:
        if (entry.title.text == 'Elizabeth Bennet' and
                    entry.content.text == 'Test Notes' and
                    entry.email[0].address == 'liz@gmail.com'):
            client.DeleteContact(entry.GetEditLink().href)


def suite():
    return unittest.TestSuite((unittest.makeSuite(ContactsServiceTest, 'test'),
                               unittest.makeSuite(ContactsQueryTest, 'test'),
                               unittest.makeSuite(ContactsGroupsTest, 'test'),))


if __name__ == '__main__':
    print('Contacts Tests\nNOTE: Please run these tests only with a test '
          'account. The tests may delete or update your data.')
    unittest.TextTestRunner().run(suite())
