#
# Copyright (C) 2007 Google Inc.
#
# Licensed under the Apache License 2.0;


# __author__ = 'api.jscudder (Jeffrey Scudder)'

import getpass
import time
import unittest

import atom
import gdata.photos
import gdata.photos.service

username = ''
password = ''
test_image_location = '../../testimage.jpg'
test_image_name = 'testimage.jpg'


class PhotosServiceTest(unittest.TestCase):
    def setUp(self):
        # Initialize the client and create a new album for testing.
        self.client = gdata.photos.service.PhotosService()
        self.client.email = username
        self.client.password = password
        self.client.source = 'Photos Client Unit Tests'
        self.client.ProgrammaticLogin()

        # Give the album a unique title by appending the current time.
        self.test_album = self.client.InsertAlbum(
            'Python library test' + str(time.time()),
            'A temporary test album.')

    def testUploadGetAndDeletePhoto(self):
        image_entry = self.client.InsertPhotoSimple(self.test_album,
                                                    'test', 'a pretty testing picture', test_image_location)
        self.assertTrue(image_entry.title.text == 'test')
        results_feed = self.client.SearchUserPhotos('test')
        self.assertTrue(len(results_feed.entry) > 0)
        self.client.Delete(image_entry)

    def testInsertPhotoUpdateBlobAndDelete(self):
        new_entry = gdata.photos.PhotoEntry()
        new_entry.title = atom.Title(text='a_test_image')
        new_entry.summary = atom.Summary(text='Just a test.')
        new_entry.category.append(atom.Category(
            scheme='http://schemas.google.com/g/2005#kind',
            term='http://schemas.google.com/photos/2007#photo'))
        entry = self.client.InsertPhoto(self.test_album, new_entry,
                                        test_image_location, content_type='image/jpeg')
        self.assertTrue(entry.id.text)
        updated_entry = self.client.UpdatePhotoBlob(entry, test_image_location)
        self.assertTrue(entry.GetEditLink().href != updated_entry.GetEditLink().href)
        self.client.Delete(updated_entry)

    def tearDown(self):
        # Delete the test album.
        test_album = self.client.GetEntry(self.test_album.GetSelfLink().href)
        self.client.Delete(test_album)


if __name__ == '__main__':
    print('Google Photos test\nNOTE: Please run these tests only with a test '
          'account. The tests may delete or update your data.')
    username = input('Please enter your username: ')
    password = getpass.getpass()
    unittest.main()
