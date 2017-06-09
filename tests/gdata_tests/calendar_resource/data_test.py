#
# Copyright (C) 2008 Google Inc.
#
# Licensed under the Apache License 2.0;



# __author__ = 'Vic Fryzel <vf@google.com>'

import unittest

import atom.core
import gdata.calendar_resource.data
import gdata.test_config as conf
from gdata import test_data


class CalendarResourceEntryTest(unittest.TestCase):
    def setUp(self):
        self.entry = atom.core.parse(test_data.CALENDAR_RESOURCE_ENTRY,
                                     gdata.calendar_resource.data.CalendarResourceEntry)
        self.feed = atom.core.parse(test_data.CALENDAR_RESOURCES_FEED,
                                    gdata.calendar_resource.data.CalendarResourceFeed)

    def testCalendarResourceEntryFromString(self):
        self.assertTrue(isinstance(self.entry,
                                   gdata.calendar_resource.data.CalendarResourceEntry))
        self.assertEqual(self.entry.resource_id, 'CR-NYC-14-12-BR')
        self.assertEqual(self.entry.resource_common_name, 'Boardroom')
        self.assertEqual(self.entry.resource_description,
                         ('This conference room is in New York City, building 14, floor 12, '
                          'Boardroom'))
        self.assertEqual(self.entry.resource_type, 'CR')

    def testCalendarResourceFeedFromString(self):
        self.assertEqual(len(self.feed.entry), 2)
        self.assertTrue(isinstance(self.feed,
                                   gdata.calendar_resource.data.CalendarResourceFeed))
        self.assertTrue(isinstance(self.feed.entry[0],
                                   gdata.calendar_resource.data.CalendarResourceEntry))
        self.assertTrue(isinstance(self.feed.entry[1],
                                   gdata.calendar_resource.data.CalendarResourceEntry))
        self.assertEqual(
            self.feed.entry[0].find_edit_link(),
            'https://apps-apis.google.com/feeds/calendar/resource/2.0/yourdomain.com/CR-NYC-14-12-BR')
        self.assertEqual(self.feed.entry[0].resource_id, 'CR-NYC-14-12-BR')
        self.assertEqual(self.feed.entry[0].resource_common_name, 'Boardroom')
        self.assertEqual(self.feed.entry[0].resource_description,
                         ('This conference room is in New York City, building 14, floor 12, '
                          'Boardroom'))
        self.assertEqual(self.feed.entry[0].resource_type, 'CR')
        self.assertEqual(self.feed.entry[1].resource_id,
                         '(Bike)-London-43-Lobby-Bike-1')
        self.assertEqual(self.feed.entry[1].resource_common_name, 'London bike-1')
        self.assertEqual(self.feed.entry[1].resource_description,
                         'Bike is in London at building 43\'s lobby.')
        self.assertEqual(self.feed.entry[1].resource_type, '(Bike)')
        self.assertEqual(
            self.feed.entry[1].find_edit_link(),
            'https://apps-apis.google.com/a/feeds/calendar/resource/2.0/yourdomain.com/(Bike)-London-43-Lobby-Bike-1')


def suite():
    return conf.build_suite([CalendarResourceEntryTest])


if __name__ == '__main__':
    unittest.main()
