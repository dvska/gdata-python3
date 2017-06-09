#
# Copyright (C) 2008 Google Inc.
#
# Licensed under the Apache License 2.0;


# __author__ = 'api.jhartmann@gmail.com (Jochen Hartmann)'

import getpass
import random
import time
import unittest

import gdata.youtube
import gdata.youtube.service

YOUTUBE_TEST_CLIENT_ID = 'ytapi-pythonclientlibrary_servicetest'


class YouTubeServiceTest(unittest.TestCase):
    def setUp(self):
        self.client = gdata.youtube.service.YouTubeService()
        self.client.email = username
        self.client.password = password
        self.client.source = YOUTUBE_TEST_CLIENT_ID
        self.client.developer_key = developer_key
        self.client.client_id = YOUTUBE_TEST_CLIENT_ID
        self.client.ProgrammaticLogin()

    def testRetrieveVideoFeed(self):
        feed = self.client.GetYouTubeVideoFeed(
            'https://gdata.youtube.com/feeds/api/standardfeeds/recently_featured');
        self.assertTrue(isinstance(feed, gdata.youtube.YouTubeVideoFeed))
        self.assertTrue(len(feed.entry) > 0)
        for entry in feed.entry:
            self.assertTrue(entry.title.text != '')

    def testRetrieveTopRatedVideoFeed(self):
        feed = self.client.GetTopRatedVideoFeed()
        self.assertTrue(isinstance(feed, gdata.youtube.YouTubeVideoFeed))
        self.assertTrue(len(feed.entry) > 10)

    def testRetrieveMostViewedVideoFeed(self):
        feed = self.client.GetMostViewedVideoFeed()
        self.assertTrue(isinstance(feed, gdata.youtube.YouTubeVideoFeed))
        self.assertTrue(len(feed.entry) > 10)

    def testRetrieveRecentlyFeaturedVideoFeed(self):
        feed = self.client.GetRecentlyFeaturedVideoFeed()
        self.assertTrue(isinstance(feed, gdata.youtube.YouTubeVideoFeed))
        self.assertTrue(len(feed.entry) > 10)

    def testRetrieveWatchOnMobileVideoFeed(self):
        feed = self.client.GetWatchOnMobileVideoFeed()
        self.assertTrue(isinstance(feed, gdata.youtube.YouTubeVideoFeed))
        self.assertTrue(len(feed.entry) > 10)

    def testRetrieveTopFavoritesVideoFeed(self):
        feed = self.client.GetTopFavoritesVideoFeed()
        self.assertTrue(isinstance(feed, gdata.youtube.YouTubeVideoFeed))
        self.assertTrue(len(feed.entry) > 10)

    def testRetrieveMostRecentVideoFeed(self):
        feed = self.client.GetMostRecentVideoFeed()
        self.assertTrue(isinstance(feed, gdata.youtube.YouTubeVideoFeed))
        self.assertTrue(len(feed.entry) > 10)

    def testRetrieveMostDiscussedVideoFeed(self):
        feed = self.client.GetMostDiscussedVideoFeed()
        self.assertTrue(isinstance(feed, gdata.youtube.YouTubeVideoFeed))
        self.assertTrue(len(feed.entry) > 10)

    def testRetrieveMostLinkedVideoFeed(self):
        feed = self.client.GetMostLinkedVideoFeed()
        self.assertTrue(isinstance(feed, gdata.youtube.YouTubeVideoFeed))
        self.assertTrue(len(feed.entry) > 10)

    def testRetrieveMostRespondedVideoFeed(self):
        feed = self.client.GetMostRespondedVideoFeed()
        self.assertTrue(isinstance(feed, gdata.youtube.YouTubeVideoFeed))
        self.assertTrue(len(feed.entry) > 10)

    def testRetrieveVideoEntryByUri(self):
        entry = self.client.GetYouTubeVideoEntry(
            'https://gdata.youtube.com/feeds/videos/Ncakifd_16k')
        self.assertTrue(isinstance(entry, gdata.youtube.YouTubeVideoEntry))
        self.assertTrue(entry.title.text != '')

    def testRetrieveVideoEntryByVideoId(self):
        entry = self.client.GetYouTubeVideoEntry(video_id='Ncakifd_16k')
        self.assertTrue(isinstance(entry, gdata.youtube.YouTubeVideoEntry))
        self.assertTrue(entry.title.text != '')

    def testRetrieveUserVideosbyUri(self):
        feed = self.client.GetYouTubeUserFeed(
            'https://gdata.youtube.com/feeds/users/gdpython/uploads')
        self.assertTrue(isinstance(feed, gdata.youtube.YouTubeVideoFeed))
        self.assertTrue(len(feed.entry) > 0)

    def testRetrieveUserVideosbyUsername(self):
        feed = self.client.GetYouTubeUserFeed(username='gdpython')
        self.assertTrue(isinstance(feed, gdata.youtube.YouTubeVideoFeed))
        self.assertTrue(len(feed.entry) > 0)

    def testSearchWithVideoQuery(self):
        query = gdata.youtube.service.YouTubeVideoQuery()
        query.vq = 'google'
        query.max_results = 8
        feed = self.client.YouTubeQuery(query)
        self.assertTrue(isinstance(feed, gdata.youtube.YouTubeVideoFeed))
        self.assertEqual(len(feed.entry), 8)

    def testDirectVideoUploadStatusUpdateAndDeletion(self):
        self.assertEqual(self.client.developer_key, developer_key)
        self.assertEqual(self.client.client_id, YOUTUBE_TEST_CLIENT_ID)
        self.assertEqual(self.client.additional_headers['X-GData-Key'],
                         'key=' + developer_key)
        self.assertEqual(self.client.additional_headers['X-Gdata-Client'],
                         YOUTUBE_TEST_CLIENT_ID)

        test_video_title = 'my cool video ' + str(random.randint(1000, 5000))
        test_video_description = 'description ' + str(random.randint(1000, 5000))

        my_media_group = gdata.media.Group(
            title=gdata.media.Title(text=test_video_title),
            description=gdata.media.Description(description_type='plain',
                                                text=test_video_description),
            keywords=gdata.media.Keywords(text='video, foo'),
            category=gdata.media.Category(
                text='Autos',
                scheme='http://gdata.youtube.com/schemas/2007/categories.cat',
                label='Autos'),
            player=None
        )
        self.assertTrue(isinstance(my_media_group, gdata.media.Group))

        # Set Geo location to 37,-122 lat, long
        where = gdata.geo.Where()
        where.set_location((37.0, -122.0))

        video_entry = gdata.youtube.YouTubeVideoEntry(media=my_media_group,
                                                      geo=where)

        self.assertTrue(isinstance(video_entry, gdata.youtube.YouTubeVideoEntry))

        new_entry = self.client.InsertVideoEntry(video_entry, video_file_location)
        self.assertTrue(isinstance(new_entry, gdata.youtube.YouTubeVideoEntry))
        self.assertEqual(new_entry.title.text, test_video_title)
        self.assertEqual(new_entry.media.description.text, test_video_description)
        self.assertTrue(new_entry.id.text)

        # check upload status also
        upload_status = self.client.CheckUploadStatus(new_entry)
        self.assertTrue(upload_status[0] != '')

        # test updating entry meta-data
        new_video_description = 'description ' + str(random.randint(1000, 5000))
        new_entry.media.description.text = new_video_description

        updated_entry = self.client.UpdateVideoEntry(new_entry)

        self.assertTrue(isinstance(updated_entry, gdata.youtube.YouTubeVideoEntry))
        self.assertEqual(updated_entry.media.description.text,
                         new_video_description)

        # sleep for 10 seconds
        time.sleep(10)

        # test to delete the entry
        value = self.client.DeleteVideoEntry(updated_entry)

        if not value:
            # sleep more and try again
            time.sleep(20)
            # test to delete the entry
            value = self.client.DeleteVideoEntry(updated_entry)

        self.assertTrue(value == True)

    def testDirectVideoUploadWithDeveloperTags(self):
        self.assertEqual(self.client.developer_key, developer_key)
        self.assertEqual(self.client.client_id, YOUTUBE_TEST_CLIENT_ID)
        self.assertEqual(self.client.additional_headers['X-GData-Key'],
                         'key=' + developer_key)
        self.assertEqual(self.client.additional_headers['X-Gdata-Client'],
                         YOUTUBE_TEST_CLIENT_ID)

        test_video_title = 'my cool video ' + str(random.randint(1000, 5000))
        test_video_description = 'description ' + str(random.randint(1000, 5000))

        test_developer_tag_01 = 'tag' + str(random.randint(1000, 5000))
        test_developer_tag_02 = 'tag' + str(random.randint(1000, 5000))
        test_developer_tag_03 = 'tag' + str(random.randint(1000, 5000))

        my_media_group = gdata.media.Group(
            title=gdata.media.Title(text=test_video_title),
            description=gdata.media.Description(description_type='plain',
                                                text=test_video_description),
            keywords=gdata.media.Keywords(text='video, foo'),
            category=[gdata.media.Category(
                text='Autos',
                scheme='http://gdata.youtube.com/schemas/2007/categories.cat',
                label='Autos')],
            player=None
        )

        self.assertTrue(isinstance(my_media_group, gdata.media.Group))

        video_entry = gdata.youtube.YouTubeVideoEntry(media=my_media_group)
        original_developer_tags = [test_developer_tag_01, test_developer_tag_02,
                                   test_developer_tag_03]

        dev_tags = video_entry.AddDeveloperTags(original_developer_tags)

        for dev_tag in dev_tags:
            self.assertTrue(dev_tag.text in original_developer_tags)

        self.assertTrue(isinstance(video_entry, gdata.youtube.YouTubeVideoEntry))

        new_entry = self.client.InsertVideoEntry(video_entry, video_file_location)

        self.assertTrue(isinstance(new_entry, gdata.youtube.YouTubeVideoEntry))
        self.assertEqual(new_entry.title.text, test_video_title)
        self.assertEqual(new_entry.media.description.text, test_video_description)
        self.assertTrue(new_entry.id.text)

        developer_tags_from_new_entry = new_entry.GetDeveloperTags()
        for dev_tag in developer_tags_from_new_entry:
            self.assertTrue(dev_tag.text in original_developer_tags)

        self.assertEqual(len(developer_tags_from_new_entry),
                         len(original_developer_tags))

        # sleep for 10 seconds
        time.sleep(10)

        # test to delete the entry
        value = self.client.DeleteVideoEntry(new_entry)

        if not value:
            # sleep more and try again
            time.sleep(20)
            # test to delete the entry
            value = self.client.DeleteVideoEntry(new_entry)

        self.assertTrue(value == True)

    def testBrowserBasedVideoUpload(self):
        self.assertEqual(self.client.developer_key, developer_key)
        self.assertEqual(self.client.client_id, YOUTUBE_TEST_CLIENT_ID)
        self.assertEqual(self.client.additional_headers['X-GData-Key'],
                         'key=' + developer_key)
        self.assertEqual(self.client.additional_headers['X-Gdata-Client'],
                         YOUTUBE_TEST_CLIENT_ID)
        test_video_title = 'my cool video ' + str(random.randint(1000, 5000))
        test_video_description = 'description ' + str(random.randint(1000, 5000))

        my_media_group = gdata.media.Group(
            title=gdata.media.Title(text=test_video_title),
            description=gdata.media.Description(description_type='plain',
                                                text=test_video_description),
            keywords=gdata.media.Keywords(text='video, foo'),
            category=gdata.media.Category(
                text='Autos',
                scheme='http://gdata.youtube.com/schemas/2007/categories.cat',
                label='Autos'),
            player=None
        )
        self.assertTrue(isinstance(my_media_group, gdata.media.Group))

        video_entry = gdata.youtube.YouTubeVideoEntry(media=my_media_group)
        self.assertTrue(isinstance(video_entry, gdata.youtube.YouTubeVideoEntry))

        response = self.client.GetFormUploadToken(video_entry)
        self.assertTrue(response[0].startswith(
            'https://uploads.gdata.youtube.com/action/FormDataUpload/'))
        self.assertTrue(len(response[0]) > 55)
        self.assertTrue(len(response[1]) > 100)

    def testRetrieveRelatedVideoFeedByUri(self):
        feed = self.client.GetYouTubeRelatedVideoFeed(
            'https://gdata.youtube.com/feeds/videos/Ncakifd_16k/related')
        self.assertTrue(isinstance(feed, gdata.youtube.YouTubeVideoFeed))
        self.assertTrue(len(feed.entry) > 0)

    def testRetrieveRelatedVideoFeedById(self):
        feed = self.client.GetYouTubeRelatedVideoFeed(video_id='Ncakifd_16k')
        self.assertTrue(isinstance(feed, gdata.youtube.YouTubeVideoFeed))
        self.assertTrue(len(feed.entry) > 0)

    def testRetrieveResponseVideoFeedByUri(self):
        feed = self.client.GetYouTubeVideoResponseFeed(
            'https://gdata.youtube.com/feeds/videos/Ncakifd_16k/responses')
        self.assertTrue(isinstance(feed, gdata.youtube.YouTubeVideoResponseFeed))
        self.assertTrue(len(feed.entry) > 0)

    def testRetrieveResponseVideoFeedById(self):
        feed = self.client.GetYouTubeVideoResponseFeed(video_id='Ncakifd_16k')
        self.assertTrue(isinstance(feed, gdata.youtube.YouTubeVideoResponseFeed))
        self.assertTrue(len(feed.entry) > 0)

    def testRetrieveVideoCommentFeedByUri(self):
        feed = self.client.GetYouTubeVideoCommentFeed(
            'https://gdata.youtube.com/feeds/api/videos/Ncakifd_16k/comments')
        self.assertTrue(isinstance(feed, gdata.youtube.YouTubeVideoCommentFeed))
        self.assertTrue(len(feed.entry) > 0)

    def testRetrieveVideoCommentFeedByVideoId(self):
        feed = self.client.GetYouTubeVideoCommentFeed(video_id='Ncakifd_16k')
        self.assertTrue(isinstance(feed, gdata.youtube.YouTubeVideoCommentFeed))
        self.assertTrue(len(feed.entry) > 0)

    def testAddComment(self):
        video_id = '9g6buYJTt_g'
        video_entry = self.client.GetYouTubeVideoEntry(video_id=video_id)
        random_comment_text = 'test_comment_' + str(random.randint(1000, 50000))
        self.client.AddComment(comment_text=random_comment_text,
                               video_entry=video_entry)
        comment_feed = self.client.GetYouTubeVideoCommentFeed(video_id=video_id)
        comment_found = False
        for item in comment_feed.entry:
            if (item.content.text == random_comment_text):
                comment_found = True
        self.assertEqual(comment_found, True)

    def testAddRating(self):
        video_id_to_rate = 'Ncakifd_16k'
        video_entry = self.client.GetYouTubeVideoEntry(video_id=video_id_to_rate)
        response = self.client.AddRating(3, video_entry)
        self.assertTrue(isinstance(response, gdata.GDataEntry))

    def testRetrievePlaylistFeedByUri(self):
        feed = self.client.GetYouTubePlaylistFeed(
            'https://gdata.youtube.com/feeds/users/gdpython/playlists')
        self.assertTrue(isinstance(feed, gdata.youtube.YouTubePlaylistFeed))
        self.assertTrue(len(feed.entry) > 0)

    def testRetrievePlaylistListFeedByUsername(self):
        feed = self.client.GetYouTubePlaylistFeed(username='gdpython')
        self.assertTrue(isinstance(feed, gdata.youtube.YouTubePlaylistFeed))
        self.assertTrue(len(feed.entry) > 0)

    def testRetrievePlaylistVideoFeed(self):
        feed = self.client.GetYouTubePlaylistVideoFeed(
            'https://gdata.youtube.com/feeds/api/playlists/BCB3BB96DF51B505')
        self.assertTrue(isinstance(feed, gdata.youtube.YouTubePlaylistVideoFeed))
        self.assertTrue(len(feed.entry) > 0)
        self.assertTrue(isinstance(feed.entry[0],
                                   gdata.youtube.YouTubePlaylistVideoEntry))

    def testAddUpdateAndDeletePlaylist(self):
        test_playlist_title = 'my test playlist ' + str(random.randint(1000, 3000))
        test_playlist_description = 'test playlist '
        response = self.client.AddPlaylist(test_playlist_title,
                                           test_playlist_description)
        self.assertTrue(isinstance(response, gdata.youtube.YouTubePlaylistEntry))

        new_playlist_title = 'my updated playlist ' + str(random.randint(1000, 4000))
        new_playlist_description = 'my updated playlist '
        playlist_entry_id = response.id.text.split('/')[-1]

        updated_playlist = self.client.UpdatePlaylist(playlist_entry_id,
                                                      new_playlist_title,
                                                      new_playlist_description)

        playlist_feed = self.client.GetYouTubePlaylistFeed()

        update_successful = False

        for playlist_entry in playlist_feed.entry:
            if playlist_entry.title.text == new_playlist_title:
                update_successful = True
                break

        self.assertEqual(update_successful, True)

        # wait
        time.sleep(10)
        # delete it
        playlist_uri = updated_playlist.id.text
        response = self.client.DeletePlaylist(playlist_uri)
        self.assertEqual(response, True)

    def testAddUpdateAndDeletePrivatePlaylist(self):
        test_playlist_title = 'my test playlist ' + str(random.randint(1000, 3000))
        test_playlist_description = 'test playlist '
        response = self.client.AddPlaylist(test_playlist_title,
                                           test_playlist_description,
                                           playlist_private=True)
        self.assertTrue(isinstance(response, gdata.youtube.YouTubePlaylistEntry))

        new_playlist_title = 'my updated playlist ' + str(random.randint(1000, 4000))
        new_playlist_description = 'my updated playlist '
        playlist_entry_id = response.id.text.split('/')[-1]

        updated_playlist = self.client.UpdatePlaylist(playlist_entry_id,
                                                      new_playlist_title,
                                                      new_playlist_description,
                                                      playlist_private=True)

        playlist_feed = self.client.GetYouTubePlaylistFeed()

        update_successful = False
        playlist_still_private = False
        for playlist_entry in playlist_feed.entry:
            if playlist_entry.title.text == new_playlist_title:
                update_successful = True
                if playlist_entry.private is not None:
                    playlist_still_private = True

        self.assertEqual(update_successful, True)
        self.assertEqual(playlist_still_private, True)

        # wait
        time.sleep(10)
        # delete it
        playlist_uri = updated_playlist.id.text
        response = self.client.DeletePlaylist(playlist_uri)
        self.assertEqual(response, True)

    def testAddEditAndDeleteVideoFromPlaylist(self):
        test_playlist_title = 'my test playlist ' + str(random.randint(1000, 3000))
        test_playlist_description = 'test playlist '
        response = self.client.AddPlaylist(test_playlist_title,
                                           test_playlist_description)
        self.assertTrue(isinstance(response, gdata.youtube.YouTubePlaylistEntry))

        custom_video_title = 'my test video on my test playlist'
        custom_video_description = 'this is a test video on my test playlist'
        video_id = 'Ncakifd_16k'
        playlist_uri = response.feed_link[0].href
        time.sleep(10)
        response = self.client.AddPlaylistVideoEntryToPlaylist(
            playlist_uri, video_id, custom_video_title, custom_video_description)

        self.assertTrue(isinstance(response, gdata.youtube.YouTubePlaylistVideoEntry))

        playlist_entry_id = response.id.text.split('/')[-1]
        playlist_uri = response.id.text.split(playlist_entry_id)[0][:-1]
        new_video_title = 'video number ' + str(random.randint(1000, 3000))
        new_video_description = 'test video'
        time.sleep(10)
        response = self.client.UpdatePlaylistVideoEntryMetaData(
            playlist_uri,
            playlist_entry_id,
            new_video_title,
            new_video_description,
            1)
        self.assertTrue(isinstance(response, gdata.youtube.YouTubePlaylistVideoEntry))
        time.sleep(10)

        playlist_entry_id = response.id.text.split('/')[-1]
        # remove video from playlist
        response = self.client.DeletePlaylistVideoEntry(playlist_uri,
                                                        playlist_entry_id)
        self.assertEqual(response, True)

        time.sleep(10)
        # delete the playlist
        response = self.client.DeletePlaylist(playlist_uri)
        self.assertEqual(response, True)

    def testRetrieveSubscriptionFeedByUri(self):
        feed = self.client.GetYouTubeSubscriptionFeed(
            'https://gdata.youtube.com/feeds/users/gdpython/subscriptions')
        self.assertTrue(isinstance(feed, gdata.youtube.YouTubeSubscriptionFeed))
        self.assertTrue(len(feed.entry) == 3)

        subscription_to_channel_found = False
        subscription_to_favorites_found = False
        subscription_to_query_found = False
        all_types_found = False

        for entry in feed.entry:
            self.assertTrue(isinstance(entry, gdata.youtube.YouTubeSubscriptionEntry))
            subscription_type = entry.GetSubscriptionType()
            if subscription_type == 'channel':
                subscription_to_channel_found = True
            elif subscription_type == 'favorites':
                subscription_to_favorites_found = True
            elif subscription_type == 'query':
                subscription_to_query_found = True

        if (subscription_to_channel_found and subscription_to_favorites_found and
                subscription_to_query_found):
            all_types_found = True

        self.assertEqual(all_types_found, True)

    def testRetrieveSubscriptionFeedByUsername(self):
        feed = self.client.GetYouTubeSubscriptionFeed(username='gdpython')
        self.assertTrue(isinstance(feed, gdata.youtube.YouTubeSubscriptionFeed))
        self.assertTrue(len(feed.entry) == 3)

        subscription_to_channel_found = False
        subscription_to_favorites_found = False
        subscription_to_query_found = False
        all_types_found = False

        for entry in feed.entry:
            self.assertTrue(isinstance(entry, gdata.youtube.YouTubeSubscriptionEntry))
            subscription_type = entry.GetSubscriptionType()
            if subscription_type == 'channel':
                subscription_to_channel_found = True
            elif subscription_type == 'favorites':
                subscription_to_favorites_found = True
            elif subscription_type == 'query':
                subscription_to_query_found = True

        if (subscription_to_channel_found and subscription_to_favorites_found and
                subscription_to_query_found):
            all_types_found = True
        self.assertEqual(all_types_found, True)

    def testRetrieveUserProfileByUri(self):
        user = self.client.GetYouTubeUserEntry(
            'https://gdata.youtube.com/feeds/users/gdpython')
        self.assertTrue(isinstance(user, gdata.youtube.YouTubeUserEntry))
        self.assertEqual(user.location.text, 'US')

    def testRetrieveUserProfileByUsername(self):
        user = self.client.GetYouTubeUserEntry(username='gdpython')
        self.assertTrue(isinstance(user, gdata.youtube.YouTubeUserEntry))
        self.assertEqual(user.location.text, 'US')

    def testRetrieveUserFavoritesFeed(self):
        feed = self.client.GetUserFavoritesFeed(username='gdpython')
        self.assertTrue(isinstance(feed, gdata.youtube.YouTubeVideoFeed))
        self.assertTrue(len(feed.entry) > 0)

    def testRetrieveDefaultUserFavoritesFeed(self):
        feed = self.client.GetUserFavoritesFeed()
        self.assertTrue(isinstance(feed, gdata.youtube.YouTubeVideoFeed))
        self.assertTrue(len(feed.entry) > 0)

    def testAddAndDeleteVideoFromFavorites(self):
        video_id = 'Ncakifd_16k'
        video_entry = self.client.GetYouTubeVideoEntry(video_id=video_id)
        response = self.client.AddVideoEntryToFavorites(video_entry)
        self.assertTrue(isinstance(response, gdata.GDataEntry))
        time.sleep(10)
        response = self.client.DeleteVideoEntryFromFavorites(video_id)
        self.assertEqual(response, True)

    def testRetrieveContactFeedByUri(self):
        feed = self.client.GetYouTubeContactFeed(
            'https://gdata.youtube.com/feeds/users/gdpython/contacts')
        self.assertTrue(isinstance(feed, gdata.youtube.YouTubeContactFeed))
        self.assertEqual(len(feed.entry), 1)

    def testRetrieveContactFeedByUsername(self):
        feed = self.client.GetYouTubeContactFeed(username='gdpython')
        self.assertTrue(isinstance(feed, gdata.youtube.YouTubeContactFeed))
        self.assertEqual(len(feed.entry), 1)


if __name__ == '__main__':
    print('NOTE: Please run these tests only with a test account. '
          'The tests may delete or update your data.')
    username = input('Please enter your username: ')
    password = getpass.getpass()
    developer_key = input('Please enter your developer key: ')
    video_file_location = input(
        'Please enter the absolute path to a video file: ')
    unittest.main()
