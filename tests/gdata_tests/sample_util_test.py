#!/usr/bin/env python
#
# Copyright (C) 2009 Google Inc.
#
# Licensed under the Apache License 2.0;



# This module is used for version 2 of the Google Data APIs.


# __author__ = 'j.s@google.com (Jeff Scudder)'

import sys
import unittest

import gdata.sample_util


class SettingsUtilTest(unittest.TestCase):
    def setUp(self):
        self.settings = gdata.sample_util.SettingsUtil()

    def test_get_param(self):
        self.assertTrue(self.settings.get_param('missing', ask=False) is None)
        self.settings.prefs['x'] = 'something'
        self.assertEqual(self.settings.get_param('x'), 'something')

    def test_get_param_from_command_line_arg(self):
        self.assertTrue('x' not in self.settings.prefs)
        self.assertTrue(self.settings.get_param('x', ask=False) is None)
        sys.argv.append('--x=something')
        self.assertEqual(self.settings.get_param('x'), 'something')
        self.assertTrue('x' not in self.settings.prefs)
        self.assertTrue('y' not in self.settings.prefs)
        self.assertTrue(self.settings.get_param('y', ask=False) is None)
        sys.argv.append('--y')
        sys.argv.append('other')
        self.assertEqual(self.settings.get_param('y', reuse=True), 'other')
        self.assertEqual(self.settings.prefs['y'], 'other')


def suite():
    return conf.build_suite([SettingsUtilTest])


if __name__ == '__main__':
    unittest.main()
