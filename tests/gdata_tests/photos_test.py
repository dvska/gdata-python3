#
# Copyright (C) 2006 Google Inc.
#
# Licensed under the Apache License 2.0;



# __author__ = 'api.jscudder (Jeffrey Scudder)'

import unittest

import gdata.photos
from gdata import test_data


class AlbumFeedTest(unittest.TestCase):
    def setUp(self):
        self.album_feed = gdata.photos.AlbumFeedFromString(test_data.ALBUM_FEED)

    def testCorrectXmlParsing(self):
        self.assertTrue(self.album_feed.id.text == 'http://picasaweb.google.com/data/feed/api/user/sample.user/albumid/1')
        self.assertTrue(self.album_feed.gphoto_id.text == '1')
        self.assertTrue(len(self.album_feed.entry) == 4)
        for entry in self.album_feed.entry:
            if entry.id.text == 'http://picasaweb.google.com/data/entry/api/user/sample.user/albumid/1/photoid/2':
                self.assertTrue(entry.summary.text == 'Blue')


class PhotoFeedTest(unittest.TestCase):
    def setUp(self):
        self.feed = gdata.photos.PhotoFeedFromString(test_data.ALBUM_FEED)

    def testCorrectXmlParsing(self):
        for entry in self.feed.entry:
            if entry.id.text == 'http://picasaweb.google.com/data/entry/api/user/sample.user/albumid/1/photoid/2':
                self.assertTrue(entry.gphoto_id.text == '2')
                self.assertTrue(entry.albumid.text == '1')
                self.assertTrue(entry.exif.flash.text == 'true')
                self.assertTrue(entry.media.title.type == 'plain')
                self.assertTrue(entry.media.title.text == 'Aqua Blue.jpg')
                self.assertTrue(len(entry.media.thumbnail) == 3)


class AnyFeedTest(unittest.TestCase):
    def setUp(self):
        self.feed = gdata.photos.AnyFeedFromString(test_data.ALBUM_FEED)

    def testEntryTypeConversion(self):
        for entry in self.feed.entry:
            if entry.id.text == 'http://picasaweb.google.com/data/feed/api/user/sample.user/albumid/':
                self.assertTrue(isinstance(entry, gdata.photos.PhotoEntry))


if __name__ == '__main__':
    unittest.main()
