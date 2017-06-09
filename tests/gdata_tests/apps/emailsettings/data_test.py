#
# Copyright (C) 2010 Google Inc.
#
# Licensed under the Apache License 2.0;



# __author__ = 'Claudio Cherubino <ccherubino@google.com>'

import unittest

import gdata.apps.emailsettings.data
import gdata.test_config as conf


class EmailSettingsLabelTest(unittest.TestCase):
    def setUp(self):
        self.entry = gdata.apps.emailsettings.data.EmailSettingsLabel()

    def testName(self):
        self.entry.name = 'test label'
        self.assertEqual(self.entry.name, 'test label')


class EmailSettingsFilterTest(unittest.TestCase):
    def setUp(self):
        self.entry = gdata.apps.emailsettings.data.EmailSettingsFilter()

    def testFrom(self):
        self.entry.from_address = 'abc@example.com'
        self.assertEqual(self.entry.from_address, 'abc@example.com')

    def testTo(self):
        self.entry.to_address = 'to@example.com'
        self.assertEqual(self.entry.to_address, 'to@example.com')

    def testFrom(self):
        self.entry.from_address = 'abc@example.com'
        self.assertEqual(self.entry.from_address, 'abc@example.com')

    def testSubject(self):
        self.entry.subject = 'Read me'
        self.assertEqual(self.entry.subject, 'Read me')

    def testHasTheWord(self):
        self.entry.has_the_word = 'important'
        self.assertEqual(self.entry.has_the_word, 'important')

    def testDoesNotHaveTheWord(self):
        self.entry.does_not_have_the_word = 'spam'
        self.assertEqual(self.entry.does_not_have_the_word, 'spam')

    def testHasAttachments(self):
        self.entry.has_attachments = True
        self.assertEqual(self.entry.has_attachments, True)

    def testLabel(self):
        self.entry.label = 'Trip reports'
        self.assertEqual(self.entry.label, 'Trip reports')

    def testMarkHasRead(self):
        self.entry.mark_has_read = True
        self.assertEqual(self.entry.mark_has_read, True)

    def testArchive(self):
        self.entry.archive = True
        self.assertEqual(self.entry.archive, True)


class EmailSettingsSendAsAliasTest(unittest.TestCase):
    def setUp(self):
        self.entry = gdata.apps.emailsettings.data.EmailSettingsSendAsAlias()

    def testName(self):
        self.entry.name = 'Sales'
        self.assertEqual(self.entry.name, 'Sales')

    def testAddress(self):
        self.entry.address = 'sales@example.com'
        self.assertEqual(self.entry.address, 'sales@example.com')

    def testReplyTo(self):
        self.entry.reply_to = 'support@example.com'
        self.assertEqual(self.entry.reply_to, 'support@example.com')

    def testMakeDefault(self):
        self.entry.make_default = True
        self.assertEqual(self.entry.make_default, True)


class EmailSettingsWebClipTest(unittest.TestCase):
    def setUp(self):
        self.entry = gdata.apps.emailsettings.data.EmailSettingsWebClip()

    def testEnable(self):
        self.entry.enable = True
        self.assertEqual(self.entry.enable, True)


class EmailSettingsForwardingTest(unittest.TestCase):
    def setUp(self):
        self.entry = gdata.apps.emailsettings.data.EmailSettingsForwarding()

    def testEnable(self):
        self.entry.enable = True
        self.assertEqual(self.entry.enable, True)

    def testForwardTo(self):
        self.entry.forward_to = 'fred@example.com'
        self.assertEqual(self.entry.forward_to, 'fred@example.com')

    def testAction(self):
        self.entry.action = 'KEEP'
        self.assertEqual(self.entry.action, 'KEEP')


class EmailSettingsPopTest(unittest.TestCase):
    def setUp(self):
        self.entry = gdata.apps.emailsettings.data.EmailSettingsPop()

    def testEnable(self):
        self.entry.enable = True
        self.assertEqual(self.entry.enable, True)

    def testForwardTo(self):
        self.entry.enable_for = 'ALL_MAIL'
        self.assertEqual(self.entry.enable_for, 'ALL_MAIL')

    def testAction(self):
        self.entry.action = 'KEEP'
        self.assertEqual(self.entry.action, 'KEEP')


class EmailSettingsImapTest(unittest.TestCase):
    def setUp(self):
        self.entry = gdata.apps.emailsettings.data.EmailSettingsImap()

    def testEnable(self):
        self.entry.enable = True
        self.assertEqual(self.entry.enable, True)


class EmailSettingsVacationResponderTest(unittest.TestCase):
    def setUp(self):
        self.entry = gdata.apps.emailsettings.data.EmailSettingsVacationResponder()

    def testEnable(self):
        self.entry.enable = True
        self.assertEqual(self.entry.enable, True)

    def testSubject(self):
        self.entry.subject = 'On vacation!'
        self.assertEqual(self.entry.subject, 'On vacation!')

    def testMessage(self):
        self.entry.message = 'See you on September 1st'
        self.assertEqual(self.entry.message, 'See you on September 1st')

    def testStartDate(self):
        self.entry.start_date = '2011-12-05'
        self.assertEqual(self.entry.start_date, '2011-12-05')

    def testEndDate(self):
        self.entry.end_date = '2011-12-06'
        self.assertEqual(self.entry.end_date, '2011-12-06')

    def testContactsOnly(self):
        self.entry.contacts_only = True
        self.assertEqual(self.entry.contacts_only, True)

    def testDomainOnly(self):
        self.entry.domain_only = True
        self.assertEqual(self.entry.domain_only, True)


class EmailSettingsSignatureTest(unittest.TestCase):
    def setUp(self):
        self.entry = gdata.apps.emailsettings.data.EmailSettingsSignature()

    def testValue(self):
        self.entry.signature_value = 'Regards, Joe'
        self.assertEqual(self.entry.signature_value, 'Regards, Joe')


class EmailSettingsLanguageTest(unittest.TestCase):
    def setUp(self):
        self.entry = gdata.apps.emailsettings.data.EmailSettingsLanguage()

    def testLanguage(self):
        self.entry.language_tag = 'es'
        self.assertEqual(self.entry.language_tag, 'es')


class EmailSettingsGeneralTest(unittest.TestCase):
    def setUp(self):
        self.entry = gdata.apps.emailsettings.data.EmailSettingsGeneral()

    def testPageSize(self):
        self.entry.page_size = 25
        self.assertEqual(self.entry.page_size, 25)

    def testShortcuts(self):
        self.entry.shortcuts = True
        self.assertEqual(self.entry.shortcuts, True)

    def testArrows(self):
        self.entry.arrows = True
        self.assertEqual(self.entry.arrows, True)

    def testSnippets(self):
        self.entry.snippets = True
        self.assertEqual(self.entry.snippets, True)

    def testUnicode(self):
        self.entry.use_unicode = True
        self.assertEqual(self.entry.use_unicode, True)


def suite():
    return conf.build_suite([EmailSettingsLabelTest, EmailSettingsFilterTest,
                             EmailSettingsSendAsAliasTest, EmailSettingsWebClipTest,
                             EmailSettingsForwardingTest, EmailSettingsPopTest,
                             EmailSettingsImapTest, EmailSettingsVacationResponderTest,
                             EmailSettingsSignatureTest, EmailSettingsLanguageTest,
                             EmailSettingsGeneralTest])


if __name__ == '__main__':
    unittest.main()
