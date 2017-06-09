#
# Copyright (C) 2006 Google Inc.
#
# Licensed under the Apache License 2.0;



# __author__ = 'api.jhartmann@gmail.com (Jochen Hartmann)'

import unittest

import gdata.youtube
import gdata.youtube.service
from gdata import test_data

YOUTUBE_TEMPLATE = '{http://gdata.youtube.com/schemas/2007}%s'
YT_FORMAT = YOUTUBE_TEMPLATE % ('format')


class VideoEntryTest(unittest.TestCase):
    def setUp(self):
        self.video_feed = gdata.youtube.YouTubeVideoFeedFromString(
            test_data.YOUTUBE_VIDEO_FEED)

    def testCorrectXmlParsing(self):
        self.assertEqual(self.video_feed.id.text,
                         'http://gdata.youtube.com/feeds/api/standardfeeds/top_rated')
        self.assertEqual(len(self.video_feed.entry), 2)
        for entry in self.video_feed.entry:
            if (entry.id.text ==
                    'http://gdata.youtube.com/feeds/api/videos/C71ypXYGho8'):
                self.assertEqual(entry.published.text, '2008-03-20T10:17:27.000-07:00')
                self.assertEqual(entry.updated.text, '2008-05-14T04:26:37.000-07:00')
                self.assertEqual(entry.category[0].scheme,
                                 'http://gdata.youtube.com/schemas/2007/keywords.cat')
                self.assertEqual(entry.category[0].term, 'karyn')
                self.assertEqual(entry.category[1].scheme,
                                 'http://gdata.youtube.com/schemas/2007/keywords.cat')
                self.assertEqual(entry.category[1].term, 'garcia')
                self.assertEqual(entry.category[2].scheme,
                                 'http://gdata.youtube.com/schemas/2007/keywords.cat')
                self.assertEqual(entry.category[2].term, 'me')
                self.assertEqual(entry.category[3].scheme,
                                 'http://schemas.google.com/g/2005#kind')
                self.assertEqual(entry.category[3].term,
                                 'http://gdata.youtube.com/schemas/2007#video')
                self.assertEqual(entry.title.text,
                                 'Me odeio por te amar - KARYN GARCIA')
                self.assertEqual(entry.content.text, 'http://www.karyngarcia.com.br')
                self.assertEqual(entry.link[0].rel, 'alternate')
                self.assertEqual(entry.link[0].href,
                                 'http://www.youtube.com/watch?v=C71ypXYGho8')
                self.assertEqual(entry.link[1].rel,
                                 'http://gdata.youtube.com/schemas/2007#video.related')
                self.assertEqual(entry.link[1].href,
                                 'http://gdata.youtube.com/feeds/api/videos/C71ypXYGho8/related')
                self.assertEqual(entry.link[2].rel, 'self')
                self.assertEqual(entry.link[2].href,
                                 ('http://gdata.youtube.com/feeds/api/standardfeeds'
                                  '/top_rated/C71ypXYGho8'))
                self.assertEqual(entry.author[0].name.text, 'TvKarynGarcia')
                self.assertEqual(entry.author[0].uri.text,
                                 'http://gdata.youtube.com/feeds/api/users/tvkaryngarcia')

                self.assertEqual(entry.media.title.text,
                                 'Me odeio por te amar - KARYN GARCIA')
                self.assertEqual(entry.media.description.text,
                                 'http://www.karyngarcia.com.br')
                self.assertEqual(entry.media.keywords.text,
                                 'amar, boyfriend, garcia, karyn, me, odeio, por, te')
                self.assertEqual(entry.media.duration.seconds, '203')
                self.assertEqual(entry.media.category[0].label, 'Music')
                self.assertEqual(entry.media.category[0].scheme,
                                 'http://gdata.youtube.com/schemas/2007/categories.cat')
                self.assertEqual(entry.media.category[0].text, 'Music')
                self.assertEqual(entry.media.category[1].label, 'test111')
                self.assertEqual(entry.media.category[1].scheme,
                                 'http://gdata.youtube.com/schemas/2007/developertags.cat')
                self.assertEqual(entry.media.category[1].text, 'test111')
                self.assertEqual(entry.media.category[2].label, 'test222')
                self.assertEqual(entry.media.category[2].scheme,
                                 'http://gdata.youtube.com/schemas/2007/developertags.cat')
                self.assertEqual(entry.media.category[2].text, 'test222')
                self.assertEqual(entry.media.content[0].url,
                                 'http://www.youtube.com/v/C71ypXYGho8')
                self.assertEqual(entry.media.content[0].type,
                                 'application/x-shockwave-flash')
                self.assertEqual(entry.media.content[0].medium, 'video')
                self.assertEqual(
                    entry.media.content[0].extension_attributes['isDefault'], 'true')
                self.assertEqual(
                    entry.media.content[0].extension_attributes['expression'], 'full')
                self.assertEqual(
                    entry.media.content[0].extension_attributes['duration'], '203')
                self.assertEqual(
                    entry.media.content[0].extension_attributes[YT_FORMAT], '5')
                self.assertEqual(entry.media.content[1].url,
                                 ('rtsp://rtsp2.youtube.com/ChoLENy73wIaEQmPhgZ2pXK9CxMYDSANFEgGDA'
                                  '==/0/0/0/video.3gp'))
                self.assertEqual(entry.media.content[1].type, 'video/3gpp')
                self.assertEqual(entry.media.content[1].medium, 'video')
                self.assertEqual(
                    entry.media.content[1].extension_attributes['expression'], 'full')
                self.assertEqual(
                    entry.media.content[1].extension_attributes['duration'], '203')
                self.assertEqual(
                    entry.media.content[1].extension_attributes[YT_FORMAT], '1')
                self.assertEqual(entry.media.content[2].url,
                                 ('rtsp://rtsp2.youtube.com/ChoLENy73wIaEQmPhgZ2pXK9CxMYESARFEgGDA=='
                                  '/0/0/0/video.3gp'))
                self.assertEqual(entry.media.content[2].type, 'video/3gpp')
                self.assertEqual(entry.media.content[2].medium, 'video')
                self.assertEqual(
                    entry.media.content[2].extension_attributes['expression'], 'full')
                self.assertEqual(
                    entry.media.content[2].extension_attributes['duration'], '203')
                self.assertEqual(
                    entry.media.content[2].extension_attributes[YT_FORMAT], '6')
                self.assertEqual(entry.media.player.url,
                                 'http://www.youtube.com/watch?v=C71ypXYGho8')
                self.assertEqual(entry.media.thumbnail[0].url,
                                 'http://img.youtube.com/vi/C71ypXYGho8/2.jpg')
                self.assertEqual(entry.media.thumbnail[0].height, '97')
                self.assertEqual(entry.media.thumbnail[0].width, '130')
                self.assertEqual(entry.media.thumbnail[0].extension_attributes['time'],
                                 '00:01:41.500')
                self.assertEqual(entry.media.thumbnail[1].url,
                                 'http://img.youtube.com/vi/C71ypXYGho8/1.jpg')
                self.assertEqual(entry.media.thumbnail[1].height, '97')
                self.assertEqual(entry.media.thumbnail[1].width, '130')
                self.assertEqual(entry.media.thumbnail[1].extension_attributes['time'],
                                 '00:00:50.750')
                self.assertEqual(entry.media.thumbnail[2].url,
                                 'http://img.youtube.com/vi/C71ypXYGho8/3.jpg')
                self.assertEqual(entry.media.thumbnail[2].height, '97')
                self.assertEqual(entry.media.thumbnail[2].width, '130')
                self.assertEqual(entry.media.thumbnail[2].extension_attributes['time'],
                                 '00:02:32.250')
                self.assertEqual(entry.media.thumbnail[3].url,
                                 'http://img.youtube.com/vi/C71ypXYGho8/0.jpg')
                self.assertEqual(entry.media.thumbnail[3].height, '240')
                self.assertEqual(entry.media.thumbnail[3].width, '320')
                self.assertEqual(entry.media.thumbnail[3].extension_attributes['time'],
                                 '00:01:41.500')

                self.assertEqual(entry.statistics.view_count, '138864')
                self.assertEqual(entry.statistics.favorite_count, '2474')
                self.assertEqual(entry.rating.min, '1')
                self.assertEqual(entry.rating.max, '5')
                self.assertEqual(entry.rating.num_raters, '4626')
                self.assertEqual(entry.rating.average, '4.95')
                self.assertEqual(entry.comments.feed_link[0].href,
                                 ('http://gdata.youtube.com/feeds/api/videos/'
                                  'C71ypXYGho8/comments'))
                self.assertEqual(entry.comments.feed_link[0].count_hint, '27')

                self.assertEqual(entry.GetSwfUrl(),
                                 'http://www.youtube.com/v/C71ypXYGho8')
                self.assertEqual(entry.GetYouTubeCategoryAsString(), 'Music')


class VideoEntryPrivateTest(unittest.TestCase):
    def setUp(self):
        self.entry = gdata.youtube.YouTubeVideoEntryFromString(
            test_data.YOUTUBE_ENTRY_PRIVATE)

    def testCorrectXmlParsing(self):
        self.assertTrue(isinstance(self.entry,
                                   gdata.youtube.YouTubeVideoEntry))
        self.assertTrue(self.entry.media.private)


class VideoFeedTest(unittest.TestCase):
    def setUp(self):
        self.feed = gdata.youtube.YouTubeVideoFeedFromString(
            test_data.YOUTUBE_VIDEO_FEED)

    def testCorrectXmlParsing(self):
        self.assertEqual(self.feed.id.text,
                         'http://gdata.youtube.com/feeds/api/standardfeeds/top_rated')
        self.assertEqual(self.feed.generator.text, 'YouTube data API')
        self.assertEqual(self.feed.generator.uri, 'http://gdata.youtube.com/')
        self.assertEqual(len(self.feed.author), 1)
        self.assertEqual(self.feed.author[0].name.text, 'YouTube')
        self.assertEqual(len(self.feed.category), 1)
        self.assertEqual(self.feed.category[0].scheme,
                         'http://schemas.google.com/g/2005#kind')
        self.assertEqual(self.feed.category[0].term,
                         'http://gdata.youtube.com/schemas/2007#video')
        self.assertEqual(self.feed.items_per_page.text, '25')
        self.assertEqual(len(self.feed.link), 4)
        self.assertEqual(self.feed.link[0].href,
                         'http://www.youtube.com/browse?s=tr')
        self.assertEqual(self.feed.link[0].rel, 'alternate')
        self.assertEqual(self.feed.link[1].href,
                         'http://gdata.youtube.com/feeds/api/standardfeeds/top_rated')
        self.assertEqual(self.feed.link[1].rel,
                         'http://schemas.google.com/g/2005#feed')
        self.assertEqual(self.feed.link[2].href,
                         ('http://gdata.youtube.com/feeds/api/standardfeeds/top_rated?'
                          'start-index=1&max-results=25'))
        self.assertEqual(self.feed.link[2].rel, 'self')
        self.assertEqual(self.feed.link[3].href,
                         ('http://gdata.youtube.com/feeds/api/standardfeeds/top_rated?'
                          'start-index=26&max-results=25'))
        self.assertEqual(self.feed.link[3].rel, 'next')
        self.assertEqual(self.feed.start_index.text, '1')
        self.assertEqual(self.feed.title.text, 'Top Rated')
        self.assertEqual(self.feed.total_results.text, '100')
        self.assertEqual(self.feed.updated.text, '2008-05-14T02:24:07.000-07:00')
        self.assertEqual(len(self.feed.entry), 2)


class YouTubePlaylistFeedTest(unittest.TestCase):
    def setUp(self):
        self.feed = gdata.youtube.YouTubePlaylistFeedFromString(
            test_data.YOUTUBE_PLAYLIST_FEED)

    def testCorrectXmlParsing(self):
        self.assertEqual(len(self.feed.entry), 1)
        self.assertEqual(
            self.feed.category[0].scheme, 'http://schemas.google.com/g/2005#kind')
        self.assertEqual(self.feed.category[0].term,
                         'http://gdata.youtube.com/schemas/2007#playlistLink')


class YouTubePlaylistEntryTest(unittest.TestCase):
    def setUp(self):
        self.feed = gdata.youtube.YouTubePlaylistFeedFromString(
            test_data.YOUTUBE_PLAYLIST_FEED)

    def testCorrectXmlParsing(self):
        for entry in self.feed.entry:
            self.assertEqual(entry.category[0].scheme,
                             'http://schemas.google.com/g/2005#kind')
            self.assertEqual(entry.category[0].term,
                             'http://gdata.youtube.com/schemas/2007#playlistLink')
            self.assertEqual(entry.description.text,
                             'My new playlist Description')
            self.assertEqual(entry.feed_link[0].href,
                             'http://gdata.youtube.com/feeds/playlists/8BCDD04DE8F771B2')
            self.assertEqual(entry.feed_link[0].rel,
                             'http://gdata.youtube.com/schemas/2007#playlist')


class YouTubePlaylistVideoFeedTest(unittest.TestCase):
    def setUp(self):
        self.feed = gdata.youtube.YouTubePlaylistVideoFeedFromString(
            test_data.YOUTUBE_PLAYLIST_VIDEO_FEED)

    def testCorrectXmlParsing(self):
        self.assertEqual(len(self.feed.entry), 1)
        self.assertEqual(self.feed.category[0].scheme,
                         'http://schemas.google.com/g/2005#kind')
        self.assertEqual(self.feed.category[0].term,
                         'http://gdata.youtube.com/schemas/2007#playlist')
        self.assertEqual(self.feed.category[1].scheme,
                         'http://gdata.youtube.com/schemas/2007/tags.cat')
        self.assertEqual(self.feed.category[1].term, 'videos')
        self.assertEqual(self.feed.category[2].scheme,
                         'http://gdata.youtube.com/schemas/2007/tags.cat')
        self.assertEqual(self.feed.category[2].term, 'python')


class YouTubePlaylistVideoEntryTest(unittest.TestCase):
    def setUp(self):
        self.feed = gdata.youtube.YouTubePlaylistVideoFeedFromString(
            test_data.YOUTUBE_PLAYLIST_VIDEO_FEED)

    def testCorrectXmlParsing(self):
        self.assertEqual(len(self.feed.entry), 1)
        for entry in self.feed.entry:
            self.assertEqual(entry.position.text, '1')


class YouTubeVideoCommentFeedTest(unittest.TestCase):
    def setUp(self):
        self.feed = gdata.youtube.YouTubeVideoCommentFeedFromString(
            test_data.YOUTUBE_COMMENT_FEED)

    def testCorrectXmlParsing(self):
        self.assertEqual(len(self.feed.category), 1)
        self.assertEqual(self.feed.category[0].scheme,
                         'http://schemas.google.com/g/2005#kind')
        self.assertEqual(self.feed.category[0].term,
                         'http://gdata.youtube.com/schemas/2007#comment')
        self.assertEqual(len(self.feed.link), 4)
        self.assertEqual(self.feed.link[0].rel, 'related')
        self.assertEqual(self.feed.link[0].href,
                         'http://gdata.youtube.com/feeds/videos/2Idhz9ef5oU')
        self.assertEqual(self.feed.link[1].rel, 'alternate')
        self.assertEqual(self.feed.link[1].href,
                         'http://www.youtube.com/watch?v=2Idhz9ef5oU')
        self.assertEqual(self.feed.link[2].rel,
                         'http://schemas.google.com/g/2005#feed')
        self.assertEqual(self.feed.link[2].href,
                         'http://gdata.youtube.com/feeds/videos/2Idhz9ef5oU/comments')
        self.assertEqual(self.feed.link[3].rel, 'self')
        self.assertEqual(self.feed.link[3].href,
                         ('http://gdata.youtube.com/feeds/videos/2Idhz9ef5oU/comments?'
                          'start-index=1&max-results=25'))
        self.assertEqual(len(self.feed.entry), 3)


class YouTubeVideoCommentEntryTest(unittest.TestCase):
    def setUp(self):
        self.feed = gdata.youtube.YouTubeVideoCommentFeedFromString(
            test_data.YOUTUBE_COMMENT_FEED)

    def testCorrectXmlParsing(self):
        self.assertEqual(len(self.feed.entry), 3)
        self.assertTrue(isinstance(self.feed.entry[0],
                                   gdata.youtube.YouTubeVideoCommentEntry))

        for entry in self.feed.entry:
            if (entry.id.text ==
                    ('http://gdata.youtube.com/feeds/videos/'
                     '2Idhz9ef5oU/comments/91F809A3DE2EB81B')):
                self.assertEqual(entry.category[0].scheme,
                                 'http://schemas.google.com/g/2005#kind')
                self.assertEqual(entry.category[0].term,
                                 'http://gdata.youtube.com/schemas/2007#comment')
                self.assertEqual(entry.link[0].href,
                                 'http://gdata.youtube.com/feeds/videos/2Idhz9ef5oU')
                self.assertEqual(entry.link[0].rel, 'related')
                self.assertEqual(entry.content.text, 'test66')


class YouTubeVideoSubscriptionFeedTest(unittest.TestCase):
    def setUp(self):
        self.feed = gdata.youtube.YouTubeSubscriptionFeedFromString(
            test_data.YOUTUBE_SUBSCRIPTION_FEED)

    def testCorrectXmlParsing(self):
        self.assertEqual(len(self.feed.category), 1)
        self.assertEqual(self.feed.category[0].scheme,
                         'http://schemas.google.com/g/2005#kind')
        self.assertEqual(self.feed.category[0].term,
                         'http://gdata.youtube.com/schemas/2007#subscription')
        self.assertEqual(len(self.feed.link), 4)
        self.assertEqual(self.feed.link[0].rel, 'related')
        self.assertEqual(self.feed.link[0].href,
                         'http://gdata.youtube.com/feeds/users/andyland74')
        self.assertEqual(self.feed.link[1].rel, 'alternate')
        self.assertEqual(self.feed.link[1].href,
                         'http://www.youtube.com/profile_subscriptions?user=andyland74')
        self.assertEqual(self.feed.link[2].rel,
                         'http://schemas.google.com/g/2005#feed')
        self.assertEqual(self.feed.link[2].href,
                         'http://gdata.youtube.com/feeds/users/andyland74/subscriptions')
        self.assertEqual(self.feed.link[3].rel, 'self')
        self.assertEqual(self.feed.link[3].href,
                         ('http://gdata.youtube.com/feeds/users/andyland74/subscriptions?'
                          'start-index=1&max-results=25'))
        self.assertEqual(len(self.feed.entry), 1)


class YouTubeVideoSubscriptionEntryTest(unittest.TestCase):
    def setUp(self):
        self.feed = gdata.youtube.YouTubeSubscriptionFeedFromString(
            test_data.YOUTUBE_SUBSCRIPTION_FEED)

    def testCorrectXmlParsing(self):
        for entry in self.feed.entry:
            self.assertEqual(len(entry.category), 2)
            self.assertEqual(entry.category[0].scheme,
                             'http://gdata.youtube.com/schemas/2007/subscriptiontypes.cat')
            self.assertEqual(entry.category[0].term, 'channel')
            self.assertEqual(entry.category[1].scheme,
                             'http://schemas.google.com/g/2005#kind')
            self.assertEqual(entry.category[1].term,
                             'http://gdata.youtube.com/schemas/2007#subscription')
            self.assertEqual(len(entry.link), 3)
            self.assertEqual(entry.link[0].href,
                             'http://gdata.youtube.com/feeds/users/andyland74')
            self.assertEqual(entry.link[0].rel, 'related')
            self.assertEqual(entry.link[1].href,
                             'http://www.youtube.com/profile_videos?user=NBC')
            self.assertEqual(entry.link[1].rel, 'alternate')
            self.assertEqual(entry.link[2].href,
                             ('http://gdata.youtube.com/feeds/users/andyland74/subscriptions/'
                              'd411759045e2ad8c'))
            self.assertEqual(entry.link[2].rel, 'self')
            self.assertEqual(len(entry.feed_link), 1)
            self.assertEqual(entry.feed_link[0].href,
                             'http://gdata.youtube.com/feeds/api/users/nbc/uploads')
            self.assertEqual(entry.feed_link[0].rel,
                             'http://gdata.youtube.com/schemas/2007#user.uploads')
            self.assertEqual(entry.username.text, 'NBC')


class YouTubeVideoResponseFeedTest(unittest.TestCase):
    def setUp(self):
        self.feed = gdata.youtube.YouTubeVideoFeedFromString(
            test_data.YOUTUBE_VIDEO_RESPONSE_FEED)

    def testCorrectXmlParsing(self):
        self.assertEqual(len(self.feed.category), 1)
        self.assertEqual(self.feed.category[0].scheme,
                         'http://schemas.google.com/g/2005#kind')
        self.assertEqual(self.feed.category[0].term,
                         'http://gdata.youtube.com/schemas/2007#video')
        self.assertEqual(len(self.feed.link), 4)
        self.assertEqual(self.feed.link[0].href,
                         'http://gdata.youtube.com/feeds/videos/2c3q9K4cHzY')
        self.assertEqual(self.feed.link[0].rel, 'related')
        self.assertEqual(self.feed.link[1].href,
                         'http://www.youtube.com/video_response_view_all?v=2c3q9K4cHzY')
        self.assertEqual(self.feed.link[1].rel, 'alternate')
        self.assertEqual(self.feed.link[2].href,
                         'http://gdata.youtube.com/feeds/videos/2c3q9K4cHzY/responses')
        self.assertEqual(self.feed.link[2].rel,
                         'http://schemas.google.com/g/2005#feed')
        self.assertEqual(self.feed.link[3].href,
                         ('http://gdata.youtube.com/feeds/videos/2c3q9K4cHzY/responses?'
                          'start-index=1&max-results=25'))
        self.assertEqual(self.feed.link[3].rel, 'self')
        self.assertEqual(len(self.feed.entry), 1)


class YouTubeVideoResponseEntryTest(unittest.TestCase):
    def setUp(self):
        self.feed = gdata.youtube.YouTubeVideoFeedFromString(
            test_data.YOUTUBE_VIDEO_RESPONSE_FEED)

    def testCorrectXmlParsing(self):
        for entry in self.feed.entry:
            self.assertTrue(isinstance(entry, gdata.youtube.YouTubeVideoEntry))


class YouTubeContactFeed(unittest.TestCase):
    def setUp(self):
        self.feed = gdata.youtube.YouTubeContactFeedFromString(
            test_data.YOUTUBE_CONTACTS_FEED)

    def testCorrectXmlParsing(self):
        self.assertEqual(len(self.feed.entry), 2)
        self.assertEqual(self.feed.category[0].scheme,
                         'http://schemas.google.com/g/2005#kind')
        self.assertEqual(self.feed.category[0].term,
                         'http://gdata.youtube.com/schemas/2007#friend')


class YouTubeContactEntry(unittest.TestCase):
    def setUp(self):
        self.feed = gdata.youtube.YouTubeContactFeedFromString(
            test_data.YOUTUBE_CONTACTS_FEED)

    def testCorrectXmlParsing(self):
        for entry in self.feed.entry:
            if (entry.id.text == ('http://gdata.youtube.com/feeds/users/'
                                  'apitestjhartmann/contacts/testjfisher')):
                self.assertEqual(entry.username.text, 'testjfisher')
                self.assertEqual(entry.status.text, 'pending')


class YouTubeUserEntry(unittest.TestCase):
    def setUp(self):
        self.feed = gdata.youtube.YouTubeUserEntryFromString(
            test_data.YOUTUBE_PROFILE)

    def testCorrectXmlParsing(self):
        self.assertEqual(self.feed.author[0].name.text, 'andyland74')
        self.assertEqual(self.feed.books.text, 'Catch-22')
        self.assertEqual(self.feed.category[0].scheme,
                         'http://gdata.youtube.com/schemas/2007/channeltypes.cat')
        self.assertEqual(self.feed.category[0].term, 'Standard')
        self.assertEqual(self.feed.category[1].scheme,
                         'http://schemas.google.com/g/2005#kind')
        self.assertEqual(self.feed.category[1].term,
                         'http://gdata.youtube.com/schemas/2007#userProfile')
        self.assertEqual(self.feed.company.text, 'Google')
        self.assertEqual(self.feed.gender.text, 'm')
        self.assertEqual(self.feed.hobbies.text, 'Testing YouTube APIs')
        self.assertEqual(self.feed.hometown.text, 'Somewhere')
        self.assertEqual(len(self.feed.feed_link), 6)
        self.assertEqual(self.feed.feed_link[0].count_hint, '4')
        self.assertEqual(self.feed.feed_link[0].href,
                         'http://gdata.youtube.com/feeds/users/andyland74/favorites')
        self.assertEqual(self.feed.feed_link[0].rel,
                         'http://gdata.youtube.com/schemas/2007#user.favorites')
        self.assertEqual(self.feed.feed_link[1].count_hint, '1')
        self.assertEqual(self.feed.feed_link[1].href,
                         'http://gdata.youtube.com/feeds/users/andyland74/contacts')
        self.assertEqual(self.feed.feed_link[1].rel,
                         'http://gdata.youtube.com/schemas/2007#user.contacts')
        self.assertEqual(self.feed.feed_link[2].count_hint, '0')
        self.assertEqual(self.feed.feed_link[2].href,
                         'http://gdata.youtube.com/feeds/users/andyland74/inbox')
        self.assertEqual(self.feed.feed_link[2].rel,
                         'http://gdata.youtube.com/schemas/2007#user.inbox')
        self.assertEqual(self.feed.feed_link[3].count_hint, None)
        self.assertEqual(self.feed.feed_link[3].href,
                         'http://gdata.youtube.com/feeds/users/andyland74/playlists')
        self.assertEqual(self.feed.feed_link[3].rel,
                         'http://gdata.youtube.com/schemas/2007#user.playlists')
        self.assertEqual(self.feed.feed_link[4].count_hint, '4')
        self.assertEqual(self.feed.feed_link[4].href,
                         'http://gdata.youtube.com/feeds/users/andyland74/subscriptions')
        self.assertEqual(self.feed.feed_link[4].rel,
                         'http://gdata.youtube.com/schemas/2007#user.subscriptions')
        self.assertEqual(self.feed.feed_link[5].count_hint, '1')
        self.assertEqual(self.feed.feed_link[5].href,
                         'http://gdata.youtube.com/feeds/users/andyland74/uploads')
        self.assertEqual(self.feed.feed_link[5].rel,
                         'http://gdata.youtube.com/schemas/2007#user.uploads')
        self.assertEqual(self.feed.first_name.text, 'andy')
        self.assertEqual(self.feed.last_name.text, 'example')
        self.assertEqual(self.feed.link[0].href,
                         'http://www.youtube.com/profile?user=andyland74')
        self.assertEqual(self.feed.link[0].rel, 'alternate')
        self.assertEqual(self.feed.link[1].href,
                         'http://gdata.youtube.com/feeds/users/andyland74')
        self.assertEqual(self.feed.link[1].rel, 'self')
        self.assertEqual(self.feed.location.text, 'US')
        self.assertEqual(self.feed.movies.text, 'Aqua Teen Hungerforce')
        self.assertEqual(self.feed.music.text, 'Elliott Smith')
        self.assertEqual(self.feed.occupation.text, 'Technical Writer')
        self.assertEqual(self.feed.published.text, '2006-10-16T00:09:45.000-07:00')
        self.assertEqual(self.feed.school.text, 'University of North Carolina')
        self.assertEqual(self.feed.statistics.last_web_access,
                         '2008-02-25T16:03:38.000-08:00')
        self.assertEqual(self.feed.statistics.subscriber_count, '1')
        self.assertEqual(self.feed.statistics.video_watch_count, '21')
        self.assertEqual(self.feed.statistics.view_count, '9')
        self.assertEqual(self.feed.thumbnail.url,
                         'http://i.ytimg.com/vi/YFbSxcdOL-w/default.jpg')
        self.assertEqual(self.feed.title.text, 'andyland74 Channel')
        self.assertEqual(self.feed.updated.text, '2008-02-26T11:48:21.000-08:00')
        self.assertEqual(self.feed.username.text, 'andyland74')


if __name__ == '__main__':
    unittest.main()
