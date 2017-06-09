#
# Copyright (C) 2008 Google Inc.
#
# Licensed under the Apache License 2.0;



# __author__ = 'api.jscudder (Jeffrey Scudder)'

import unittest

import atom
import gdata.contacts
from gdata import test_data


class ContactEntryTest(unittest.TestCase):
    def setUp(self):
        self.entry = gdata.contacts.ContactEntryFromString(test_data.NEW_CONTACT)

    def testParsingTestEntry(self):
        self.assertEqual(self.entry.title.text, 'Fitzgerald')
        self.assertEqual(len(self.entry.email), 2)
        for email in self.entry.email:
            if email.rel == 'http://schemas.google.com/g/2005#work':
                self.assertEqual(email.address, 'liz@gmail.com')
            elif email.rel == 'http://schemas.google.com/g/2005#home':
                self.assertEqual(email.address, 'liz@example.org')
        self.assertEqual(len(self.entry.phone_number), 3)
        self.assertEqual(len(self.entry.postal_address), 1)
        self.assertEqual(self.entry.postal_address[0].primary, 'true')
        self.assertEqual(self.entry.postal_address[0].text,
                         '1600 Amphitheatre Pkwy Mountain View')
        self.assertEqual(len(self.entry.im), 1)
        self.assertEqual(len(self.entry.group_membership_info), 1)
        self.assertEqual(self.entry.group_membership_info[0].href,
                         'http://google.com/m8/feeds/groups/liz%40gmail.com/base/270f')
        self.assertEqual(self.entry.group_membership_info[0].deleted, 'false')
        self.assertEqual(len(self.entry.extended_property), 2)
        self.assertEqual(self.entry.extended_property[0].name, 'pet')
        self.assertEqual(self.entry.extended_property[0].value, 'hamster')
        self.assertEqual(self.entry.extended_property[1].name, 'cousine')
        self.assertEqual(
            self.entry.extended_property[1].GetXmlBlobExtensionElement().tag,
            'italian')

    def testToAndFromString(self):
        copied_entry = gdata.contacts.ContactEntryFromString(str(self.entry))
        self.assertEqual(copied_entry.title.text, 'Fitzgerald')
        self.assertEqual(len(copied_entry.email), 2)
        for email in copied_entry.email:
            if email.rel == 'http://schemas.google.com/g/2005#work':
                self.assertEqual(email.address, 'liz@gmail.com')
            elif email.rel == 'http://schemas.google.com/g/2005#home':
                self.assertEqual(email.address, 'liz@example.org')
        self.assertEqual(len(copied_entry.phone_number), 3)
        self.assertEqual(len(copied_entry.postal_address), 1)
        self.assertEqual(copied_entry.postal_address[0].primary, 'true')
        self.assertEqual(copied_entry.postal_address[0].text,
                         '1600 Amphitheatre Pkwy Mountain View')
        self.assertEqual(len(copied_entry.im), 1)
        self.assertEqual(len(copied_entry.group_membership_info), 1)
        self.assertEqual(copied_entry.group_membership_info[0].href,
                         'http://google.com/m8/feeds/groups/liz%40gmail.com/base/270f')
        self.assertEqual(copied_entry.group_membership_info[0].deleted, 'false')
        self.assertEqual(len(copied_entry.extended_property), 2)
        self.assertEqual(copied_entry.extended_property[0].name, 'pet')
        self.assertEqual(copied_entry.extended_property[0].value, 'hamster')
        self.assertEqual(copied_entry.extended_property[1].name, 'cousine')
        self.assertEqual(
            copied_entry.extended_property[1].GetXmlBlobExtensionElement().tag,
            'italian')

    def testCreateContactFromScratch(self):
        # Create a new entry
        new_entry = gdata.contacts.ContactEntry()
        new_entry.title = atom.Title(text='Elizabeth Bennet')
        new_entry.content = atom.Content(text='Test Notes')
        new_entry.email.append(gdata.contacts.Email(
            rel='http://schemas.google.com/g/2005#work',
            address='liz@gmail.com'))
        new_entry.phone_number.append(gdata.contacts.PhoneNumber(
            rel='http://schemas.google.com/g/2005#work', text='(206)555-1212'))
        new_entry.organization = gdata.contacts.Organization(
            org_name=gdata.contacts.OrgName(text='TestCo.'))
        new_entry.extended_property.append(gdata.ExtendedProperty(name='test',
                                                                  value='1234'))
        new_entry.birthday = gdata.contacts.Birthday(when='2009-7-23')
        sports_property = gdata.ExtendedProperty(name='sports')
        sports_property.SetXmlBlob('<dance><salsa/><ballroom_dancing/></dance>')
        new_entry.extended_property.append(sports_property)

        # Generate and parse the XML for the new entry.
        entry_copy = gdata.contacts.ContactEntryFromString(str(new_entry))
        self.assertEqual(entry_copy.title.text, new_entry.title.text)
        self.assertEqual(entry_copy.content.text, 'Test Notes')
        self.assertEqual(len(entry_copy.email), 1)
        self.assertEqual(entry_copy.email[0].rel, new_entry.email[0].rel)
        self.assertEqual(entry_copy.email[0].address, 'liz@gmail.com')
        self.assertEqual(len(entry_copy.phone_number), 1)
        self.assertEqual(entry_copy.phone_number[0].rel,
                         new_entry.phone_number[0].rel)
        self.assertEqual(entry_copy.birthday.when, '2009-7-23')
        self.assertEqual(entry_copy.phone_number[0].text, '(206)555-1212')
        self.assertEqual(entry_copy.organization.org_name.text, 'TestCo.')
        self.assertEqual(len(entry_copy.extended_property), 2)
        self.assertEqual(entry_copy.extended_property[0].name, 'test')
        self.assertEqual(entry_copy.extended_property[0].value, '1234')


class ContactsFeedTest(unittest.TestCase):
    def setUp(self):
        self.feed = gdata.contacts.ContactsFeedFromString(test_data.CONTACTS_FEED)

    def testParsingTestFeed(self):
        self.assertEqual(self.feed.id.text,
                         'http://www.google.com/m8/feeds/contacts/liz%40gmail.com/base')
        self.assertEqual(self.feed.title.text, 'Contacts')
        self.assertEqual(self.feed.total_results.text, '1')
        self.assertEqual(len(self.feed.entry), 1)
        self.assertTrue(isinstance(self.feed.entry[0], gdata.contacts.ContactEntry))
        self.assertEqual(self.feed.entry[0].GetPhotoLink().href,
                         'http://google.com/m8/feeds/photos/media/liz%40gmail.com/c9012de')
        self.assertEqual(self.feed.entry[0].GetPhotoEditLink().href,
                         'http://www.google.com/m8/feeds/photos/media/liz%40gmail.com/'
                         'c9012de/photo4524')

    def testToAndFromString(self):
        copied_feed = gdata.contacts.ContactsFeedFromString(str(self.feed))
        self.assertEqual(copied_feed.id.text,
                         'http://www.google.com/m8/feeds/contacts/liz%40gmail.com/base')
        self.assertEqual(copied_feed.title.text, 'Contacts')
        self.assertEqual(copied_feed.total_results.text, '1')
        self.assertEqual(len(copied_feed.entry), 1)
        self.assertTrue(isinstance(copied_feed.entry[0], gdata.contacts.ContactEntry))


class GroupsFeedTest(unittest.TestCase):
    def setUp(self):
        self.feed = gdata.contacts.GroupsFeedFromString(
            test_data.CONTACT_GROUPS_FEED)

    def testParsingGroupsFeed(self):
        self.assertEqual(self.feed.id.text, 'jo@gmail.com')
        self.assertEqual(self.feed.title.text, 'Jo\'s Contact Groups')
        self.assertEqual(self.feed.total_results.text, '3')
        self.assertEqual(len(self.feed.entry), 1)
        self.assertTrue(isinstance(self.feed.entry[0], gdata.contacts.GroupEntry))


class GroupEntryTest(unittest.TestCase):
    def setUp(self):
        self.entry = gdata.contacts.GroupEntryFromString(
            test_data.CONTACT_GROUP_ENTRY)

    def testParsingTestEntry(self):
        self.assertEqual(self.entry.title.text, 'Salsa group')
        self.assertEqual(len(self.entry.extended_property), 1)
        self.assertEqual(self.entry.extended_property[0].name,
                         'more info about the group')
        self.assertEqual(
            self.entry.extended_property[0].GetXmlBlobExtensionElement().namespace,
            atom.ATOM_NAMESPACE)
        self.assertEqual(
            self.entry.extended_property[0].GetXmlBlobExtensionElement().tag,
            'info')
        self.assertEqual(
            self.entry.extended_property[0].GetXmlBlobExtensionElement().text,
            'Very nice people.')


if __name__ == '__main__':
    unittest.main()
