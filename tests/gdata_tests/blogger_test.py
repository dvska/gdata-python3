#
# Copyright (C) 2008 Google Inc.
#
# Licensed under the Apache License 2.0;



# __author__ = 'api.jscudder (Jeff Scudder)'

import unittest

import atom
import gdata.blogger
from gdata import test_data


class BlogEntryTest(unittest.TestCase):
    def testBlogEntryFromString(self):
        entry = gdata.blogger.BlogEntryFromString(test_data.BLOG_ENTRY)
        self.assertEqual(entry.GetBlogName(), 'blogName')
        self.assertEqual(entry.GetBlogId(), 'blogID')
        self.assertEqual(entry.title.text, 'Lizzy\'s Diary')

    def testBlogPostFeedFromString(self):
        feed = gdata.blogger.BlogPostFeedFromString(test_data.BLOG_POSTS_FEED)
        self.assertEqual(len(feed.entry), 1)
        self.assertTrue(isinstance(feed, gdata.blogger.BlogPostFeed))
        self.assertTrue(isinstance(feed.entry[0], gdata.blogger.BlogPostEntry))
        self.assertEqual(feed.entry[0].GetPostId(), 'postID')
        self.assertEqual(feed.entry[0].GetBlogId(), 'blogID')
        self.assertEqual(feed.entry[0].title.text, 'Quite disagreeable')

    def testCommentFeedFromString(self):
        feed = gdata.blogger.CommentFeedFromString(test_data.BLOG_COMMENTS_FEED)
        self.assertEqual(len(feed.entry), 1)
        self.assertTrue(isinstance(feed, gdata.blogger.CommentFeed))
        self.assertTrue(isinstance(feed.entry[0], gdata.blogger.CommentEntry))
        self.assertEqual(feed.entry[0].GetBlogId(), 'blogID')
        self.assertEqual(feed.entry[0].GetCommentId(), 'commentID')
        self.assertEqual(feed.entry[0].title.text, 'This is my first comment')
        self.assertEqual(feed.entry[0].in_reply_to.source,
                         'http://blogName.blogspot.com/feeds/posts/default/postID')
        self.assertEqual(feed.entry[0].in_reply_to.ref,
                         'tag:blogger.com,1999:blog-blogID.post-postID')
        self.assertEqual(feed.entry[0].in_reply_to.href,
                         'http://blogName.blogspot.com/2007/04/first-post.html')
        self.assertEqual(feed.entry[0].in_reply_to.type, 'text/html')

    def testIdParsing(self):
        entry = gdata.blogger.BlogEntry()
        entry.id = atom.Id(
            text='tag:blogger.com,1999:user-146606542.blog-4023408167658848')
        self.assertEqual(entry.GetBlogId(), '4023408167658848')
        entry.id = atom.Id(text='tag:blogger.com,1999:blog-4023408167658848')
        self.assertEqual(entry.GetBlogId(), '4023408167658848')


class InReplyToTest(unittest.TestCase):
    def testToAndFromString(self):
        in_reply_to = gdata.blogger.InReplyTo(href='http://example.com/href',
                                              ref='http://example.com/ref', source='http://example.com/my_post',
                                              type='text/html')
        xml_string = str(in_reply_to)
        parsed = gdata.blogger.InReplyToFromString(xml_string)
        self.assertEqual(parsed.source, in_reply_to.source)
        self.assertEqual(parsed.href, in_reply_to.href)
        self.assertEqual(parsed.ref, in_reply_to.ref)
        self.assertEqual(parsed.type, in_reply_to.type)


class CommentEntryTest(unittest.TestCase):
    def testToAndFromString(self):
        comment = gdata.blogger.CommentEntry(content=atom.Content(text='Nifty!'),
                                             in_reply_to=gdata.blogger.InReplyTo(
                                                 source='http://example.com/my_post'))
        parsed = gdata.blogger.CommentEntryFromString(str(comment))
        self.assertEqual(parsed.in_reply_to.source, comment.in_reply_to.source)
        self.assertEqual(parsed.content.text, comment.content.text)


if __name__ == '__main__':
    unittest.main()
