#
# Copyright (C) 2008 Google
#
# Licensed under the Apache License 2.0;


"""Test for Email Settings service."""

# __author__ = 'google-apps-apis@googlegroups.com'

import getpass
import unittest

import gdata.apps.emailsettings.service

domain = ''
admin_email = ''
admin_password = ''
username = ''


class EmailSettingsTest(unittest.TestCase):
    """Test for the EmailSettingsService."""

    def setUp(self):
        self.es = gdata.apps.emailsettings.service.EmailSettingsService(
            email=admin_email, password=admin_password, domain=domain)
        self.es.ProgrammaticLogin()

    def testCreateLabel(self):
        result = self.es.CreateLabel(username, label='New label!!!')
        self.assertEqual(result['label'], 'New label!!!')

    def testCreateFilter(self):
        result = self.es.CreateFilter(username,
                                      from_='from_foo',
                                      to='to_foo',
                                      subject='subject_foo',
                                      has_the_word='has_the_words_foo',
                                      does_not_have_the_word='doesnt_have_foo',
                                      has_attachment=True,
                                      label='label_foo',
                                      should_mark_as_read=True,
                                      should_archive=True)
        self.assertEqual(result['from'], 'from_foo')
        self.assertEqual(result['to'], 'to_foo')
        self.assertEqual(result['subject'], 'subject_foo')

    def testCreateSendAsAlias(self):
        result = self.es.CreateSendAsAlias(username,
                                           name='Send-as Alias',
                                           address='user2@sizzles.org',
                                           reply_to='user3@sizzles.org',
                                           make_default=True)
        self.assertEqual(result['name'], 'Send-as Alias')

    def testUpdateWebClipSettings(self):
        result = self.es.UpdateWebClipSettings(username, enable=True)
        self.assertEqual(result['enable'], 'true')

    def testUpdateForwarding(self):
        result = self.es.UpdateForwarding(username,
                                          enable=True,
                                          forward_to='user4@sizzles.org',
                                          action=gdata.apps.emailsettings.service.KEEP)
        self.assertEqual(result['enable'], 'true')

    def testUpdatePop(self):
        result = self.es.UpdatePop(username,
                                   enable=True,
                                   enable_for=gdata.apps.emailsettings.service.ALL_MAIL,
                                   action=gdata.apps.emailsettings.service.ARCHIVE)
        self.assertEqual(result['enable'], 'true')

    def testUpdateImap(self):
        result = self.es.UpdateImap(username, enable=True)
        self.assertEqual(result['enable'], 'true')

    def testUpdateVacation(self):
        result = self.es.UpdateVacation(username,
                                        enable=True,
                                        subject='Hawaii',
                                        message='Wish you were here!',
                                        contacts_only=True)
        self.assertEqual(result['subject'], 'Hawaii')

    def testUpdateSignature(self):
        result = self.es.UpdateSignature(username, signature='Signature')
        self.assertEqual(result['signature'], 'Signature')

    def testUpdateLanguage(self):
        result = self.es.UpdateLanguage(username, language='fr')
        self.assertEqual(result['language'], 'fr')

    def testUpdateGeneral(self):
        result = self.es.UpdateGeneral(username,
                                       page_size=100,
                                       shortcuts=True,
                                       arrows=True,
                                       snippets=True,
                                       str=True)
        self.assertEqual(result['pageSize'], '100')


if __name__ == '__main__':
    print("""Google Apps Email Settings Service Tests

NOTE: Please run these tests only with a test user account.
""")
    domain = input('Google Apps domain: ')
    admin_email = '%s@%s' % (input('Administrator username: '), domain)
    admin_password = getpass.getpass('Administrator password: ')
    username = input('Test username: ')
    unittest.main()
