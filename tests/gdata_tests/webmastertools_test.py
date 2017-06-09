#
# Copyright (C) 2008 Yu-Jie Lin
#
# Licensed under the Apache License 2.0;



# __author__ = 'livibetter (Yu-Jie Lin)'

import unittest

import gdata
import gdata.webmastertools as webmastertools
from gdata import test_data


class IndexedTest(unittest.TestCase):
    def setUp(self):
        self.indexed = webmastertools.Indexed()

    def testToAndFromString(self):
        self.indexed.text = 'true'
        self.assertTrue(self.indexed.text == 'true')
        new_indexed = webmastertools.IndexedFromString(self.indexed.ToString())
        self.assertTrue(self.indexed.text == new_indexed.text)


class CrawledTest(unittest.TestCase):
    def setUp(self):
        self.crawled = webmastertools.Crawled()

    def testToAndFromString(self):
        self.crawled.text = 'true'
        self.assertTrue(self.crawled.text == 'true')
        new_crawled = webmastertools.CrawledFromString(self.crawled.ToString())
        self.assertTrue(self.crawled.text == new_crawled.text)


class GeoLocationTest(unittest.TestCase):
    def setUp(self):
        self.geolocation = webmastertools.GeoLocation()

    def testToAndFromString(self):
        self.geolocation.text = 'US'
        self.assertTrue(self.geolocation.text == 'US')
        new_geolocation = webmastertools.GeoLocationFromString(
            self.geolocation.ToString())
        self.assertTrue(self.geolocation.text == new_geolocation.text)


class PreferredDomainTest(unittest.TestCase):
    def setUp(self):
        self.preferred_domain = webmastertools.PreferredDomain()

    def testToAndFromString(self):
        self.preferred_domain.text = 'none'
        self.assertTrue(self.preferred_domain.text == 'none')
        new_preferred_domain = webmastertools.PreferredDomainFromString(
            self.preferred_domain.ToString())
        self.assertTrue(self.preferred_domain.text == new_preferred_domain.text)


class CrawlRateTest(unittest.TestCase):
    def setUp(self):
        self.crawl_rate = webmastertools.CrawlRate()

    def testToAndFromString(self):
        self.crawl_rate.text = 'normal'
        self.assertTrue(self.crawl_rate.text == 'normal')
        new_crawl_rate = webmastertools.CrawlRateFromString(
            self.crawl_rate.ToString())
        self.assertTrue(self.crawl_rate.text == new_crawl_rate.text)


class EnhancedImageSearchTest(unittest.TestCase):
    def setUp(self):
        self.enhanced_image_search = webmastertools.EnhancedImageSearch()

    def testToAndFromString(self):
        self.enhanced_image_search.text = 'true'
        self.assertTrue(self.enhanced_image_search.text == 'true')
        new_enhanced_image_search = webmastertools.EnhancedImageSearchFromString(
            self.enhanced_image_search.ToString())
        self.assertTrue(self.enhanced_image_search.text ==
                        new_enhanced_image_search.text)


class VerifiedTest(unittest.TestCase):
    def setUp(self):
        self.verified = webmastertools.Verified()

    def testToAndFromString(self):
        self.verified.text = 'true'
        self.assertTrue(self.verified.text == 'true')
        new_verified = webmastertools.VerifiedFromString(self.verified.ToString())
        self.assertTrue(self.verified.text == new_verified.text)


class VerificationMethodMetaTest(unittest.TestCase):
    def setUp(self):
        self.meta = webmastertools.VerificationMethodMeta()

    def testToAndFromString(self):
        self.meta.name = 'verify-vf1'
        self.meta.content = 'a2Ai'
        self.assertTrue(self.meta.name == 'verify-vf1')
        self.assertTrue(self.meta.content == 'a2Ai')
        new_meta = webmastertools.VerificationMethodMetaFromString(
            self.meta.ToString())
        self.assertTrue(self.meta.name == new_meta.name)
        self.assertTrue(self.meta.content == new_meta.content)


class VerificationMethodTest(unittest.TestCase):
    def setUp(self):
        pass

    def testMetaTagToAndFromString(self):
        self.method = webmastertools.VerificationMethod()
        self.method.type = 'metatag'
        self.method.in_use = 'false'
        self.assertTrue(self.method.type == 'metatag')
        self.assertTrue(self.method.in_use == 'false')
        self.method.meta = webmastertools.VerificationMethodMeta(name='verify-vf1',
                                                                 content='a2Ai')
        self.assertTrue(self.method.meta.name == 'verify-vf1')
        self.assertTrue(self.method.meta.content == 'a2Ai')
        new_method = webmastertools.VerificationMethodFromString(
            self.method.ToString())
        self.assertTrue(self.method.type == new_method.type)
        self.assertTrue(self.method.in_use == new_method.in_use)
        self.assertTrue(self.method.meta.name == new_method.meta.name)
        self.assertTrue(self.method.meta.content == new_method.meta.content)

        method = webmastertools.VerificationMethod(type='xyz')
        self.assertEqual(method.type, 'xyz')
        method = webmastertools.VerificationMethod()
        self.assertTrue(method.type is None)

    def testHtmlPageToAndFromString(self):
        self.method = webmastertools.VerificationMethod()
        self.method.type = 'htmlpage'
        self.method.in_use = 'false'
        self.method.text = '456456-google.html'
        self.assertTrue(self.method.type == 'htmlpage')
        self.assertTrue(self.method.in_use == 'false')
        self.assertTrue(self.method.text == '456456-google.html')
        self.assertTrue(self.method.meta is None)
        new_method = webmastertools.VerificationMethodFromString(
            self.method.ToString())
        self.assertTrue(self.method.type == new_method.type)
        self.assertTrue(self.method.in_use == new_method.in_use)
        self.assertTrue(self.method.text == new_method.text)
        self.assertTrue(self.method.meta is None)

    def testConvertActualData(self):
        feed = webmastertools.SitesFeedFromString(test_data.SITES_FEED)
        self.assertTrue(len(feed.entry[0].verification_method) == 2)
        check = 0
        for method in feed.entry[0].verification_method:
            self.assertTrue(isinstance(method, webmastertools.VerificationMethod))
            if method.type == 'metatag':
                self.assertTrue(method.in_use == 'false')
                self.assertTrue(method.text is None)
                self.assertTrue(method.meta.name == 'verify-v1')
                self.assertTrue(method.meta.content == 'a2Ai')
                check = check | 1
            elif method.type == 'htmlpage':
                self.assertTrue(method.in_use == 'false')
                self.assertTrue(method.text == '456456-google.html')
                check = check | 2
            else:
                self.fail('Wrong Verification Method: %s' % method.type)
        self.assertTrue(check == 2 ** 2 - 1,
                        'Should only have two Verification Methods, metatag and htmlpage')


class MarkupLanguageTest(unittest.TestCase):
    def setUp(self):
        self.markup_language = webmastertools.MarkupLanguage()

    def testToAndFromString(self):
        self.markup_language.text = 'HTML'
        self.assertTrue(self.markup_language.text == 'HTML')
        new_markup_language = webmastertools.MarkupLanguageFromString(
            self.markup_language.ToString())
        self.assertTrue(self.markup_language.text == new_markup_language.text)


class SitemapMobileTest(unittest.TestCase):
    def setUp(self):
        self.sitemap_mobile = webmastertools.SitemapMobile()

    def testToAndFromString(self):
        self.sitemap_mobile.markup_language.append(webmastertools.MarkupLanguage(
            text='HTML'))
        self.assertTrue(self.sitemap_mobile.text is None)
        self.assertTrue(self.sitemap_mobile.markup_language[0].text == 'HTML')
        new_sitemap_mobile = webmastertools.SitemapMobileFromString(
            self.sitemap_mobile.ToString())
        self.assertTrue(new_sitemap_mobile.text is None)
        self.assertTrue(self.sitemap_mobile.markup_language[0].text ==
                        new_sitemap_mobile.markup_language[0].text)

    def testConvertActualData(self):
        feed = webmastertools.SitemapsFeedFromString(test_data.SITEMAPS_FEED)
        self.assertTrue(feed.sitemap_mobile.text.strip() == '')
        self.assertTrue(len(feed.sitemap_mobile.markup_language) == 2)
        check = 0
        for markup_language in feed.sitemap_mobile.markup_language:
            self.assertTrue(isinstance(markup_language, webmastertools.MarkupLanguage))
            if markup_language.text == "HTML":
                check = check | 1
            elif markup_language.text == "WAP":
                check = check | 2
            else:
                self.fail('Unexpected markup language: %s' % markup_language.text)
        self.assertTrue(check == 2 ** 2 - 1, "Something is wrong with markup language")


class SitemapMobileMarkupLanguageTest(unittest.TestCase):
    def setUp(self):
        self.sitemap_mobile_markup_language = \
            webmastertools.SitemapMobileMarkupLanguage()

    def testToAndFromString(self):
        self.sitemap_mobile_markup_language.text = 'HTML'
        self.assertTrue(self.sitemap_mobile_markup_language.text == 'HTML')
        new_sitemap_mobile_markup_language = \
            webmastertools.SitemapMobileMarkupLanguageFromString(
                self.sitemap_mobile_markup_language.ToString())
        self.assertTrue(self.sitemap_mobile_markup_language.text == \
                        new_sitemap_mobile_markup_language.text)


class PublicationLabelTest(unittest.TestCase):
    def setUp(self):
        self.publication_label = webmastertools.PublicationLabel()

    def testToAndFromString(self):
        self.publication_label.text = 'Value1'
        self.assertTrue(self.publication_label.text == 'Value1')
        new_publication_label = webmastertools.PublicationLabelFromString(
            self.publication_label.ToString())
        self.assertTrue(self.publication_label.text == new_publication_label.text)


class SitemapNewsTest(unittest.TestCase):
    def setUp(self):
        self.sitemap_news = webmastertools.SitemapNews()

    def testToAndFromString(self):
        self.sitemap_news.publication_label.append(webmastertools.PublicationLabel(
            text='Value1'))
        self.assertTrue(self.sitemap_news.text is None)
        self.assertTrue(self.sitemap_news.publication_label[0].text == 'Value1')
        new_sitemap_news = webmastertools.SitemapNewsFromString(
            self.sitemap_news.ToString())
        self.assertTrue(new_sitemap_news.text is None)
        self.assertTrue(self.sitemap_news.publication_label[0].text ==
                        new_sitemap_news.publication_label[0].text)

    def testConvertActualData(self):
        feed = webmastertools.SitemapsFeedFromString(test_data.SITEMAPS_FEED)
        self.assertTrue(len(feed.sitemap_news.publication_label) == 3)
        check = 0
        for publication_label in feed.sitemap_news.publication_label:
            if publication_label.text == "Value1":
                check = check | 1
            elif publication_label.text == "Value2":
                check = check | 2
            elif publication_label.text == "Value3":
                check = check | 4
            else:
                self.fail('Unexpected publication label: %s' % markup_language.text)
        self.assertTrue(check == 2 ** 3 - 1,
                        'Something is wrong with publication label')


class SitemapNewsPublicationLabelTest(unittest.TestCase):
    def setUp(self):
        self.sitemap_news_publication_label = \
            webmastertools.SitemapNewsPublicationLabel()

    def testToAndFromString(self):
        self.sitemap_news_publication_label.text = 'LabelValue'
        self.assertTrue(self.sitemap_news_publication_label.text == 'LabelValue')
        new_sitemap_news_publication_label = \
            webmastertools.SitemapNewsPublicationLabelFromString(
                self.sitemap_news_publication_label.ToString())
        self.assertTrue(self.sitemap_news_publication_label.text == \
                        new_sitemap_news_publication_label.text)


class SitemapLastDownloadedTest(unittest.TestCase):
    def setUp(self):
        self.sitemap_last_downloaded = webmastertools.SitemapLastDownloaded()

    def testToAndFromString(self):
        self.sitemap_last_downloaded.text = '2006-11-18T19:27:32.543Z'
        self.assertTrue(self.sitemap_last_downloaded.text == \
                        '2006-11-18T19:27:32.543Z')
        new_sitemap_last_downloaded = \
            webmastertools.SitemapLastDownloadedFromString(
                self.sitemap_last_downloaded.ToString())
        self.assertTrue(self.sitemap_last_downloaded.text == \
                        new_sitemap_last_downloaded.text)


class SitemapTypeTest(unittest.TestCase):
    def setUp(self):
        self.sitemap_type = webmastertools.SitemapType()

    def testToAndFromString(self):
        self.sitemap_type.text = 'WEB'
        self.assertTrue(self.sitemap_type.text == 'WEB')
        new_sitemap_type = webmastertools.SitemapTypeFromString(
            self.sitemap_type.ToString())
        self.assertTrue(self.sitemap_type.text == new_sitemap_type.text)


class SitemapStatusTest(unittest.TestCase):
    def setUp(self):
        self.sitemap_status = webmastertools.SitemapStatus()

    def testToAndFromString(self):
        self.sitemap_status.text = 'Pending'
        self.assertTrue(self.sitemap_status.text == 'Pending')
        new_sitemap_status = webmastertools.SitemapStatusFromString(
            self.sitemap_status.ToString())
        self.assertTrue(self.sitemap_status.text == new_sitemap_status.text)


class SitemapUrlCountTest(unittest.TestCase):
    def setUp(self):
        self.sitemap_url_count = webmastertools.SitemapUrlCount()

    def testToAndFromString(self):
        self.sitemap_url_count.text = '0'
        self.assertTrue(self.sitemap_url_count.text == '0')
        new_sitemap_url_count = webmastertools.SitemapUrlCountFromString(
            self.sitemap_url_count.ToString())
        self.assertTrue(self.sitemap_url_count.text == new_sitemap_url_count.text)


class SitesEntryTest(unittest.TestCase):
    def setUp(self):
        pass

    def testToAndFromString(self):
        entry = webmastertools.SitesEntry(
            indexed=webmastertools.Indexed(text='true'),
            crawled=webmastertools.Crawled(text='2008-09-14T08:59:28.000'),
            geolocation=webmastertools.GeoLocation(text='US'),
            preferred_domain=webmastertools.PreferredDomain(text='none'),
            crawl_rate=webmastertools.CrawlRate(text='normal'),
            enhanced_image_search=webmastertools.EnhancedImageSearch(text='true'),
            verified=webmastertools.Verified(text='false'),
        )
        self.assertTrue(entry.indexed.text == 'true')
        self.assertTrue(entry.crawled.text == '2008-09-14T08:59:28.000')
        self.assertTrue(entry.geolocation.text == 'US')
        self.assertTrue(entry.preferred_domain.text == 'none')
        self.assertTrue(entry.crawl_rate.text == 'normal')
        self.assertTrue(entry.enhanced_image_search.text == 'true')
        self.assertTrue(entry.verified.text == 'false')
        new_entry = webmastertools.SitesEntryFromString(entry.ToString())
        self.assertTrue(new_entry.indexed.text == 'true')
        self.assertTrue(new_entry.crawled.text == '2008-09-14T08:59:28.000')
        self.assertTrue(new_entry.geolocation.text == 'US')
        self.assertTrue(new_entry.preferred_domain.text == 'none')
        self.assertTrue(new_entry.crawl_rate.text == 'normal')
        self.assertTrue(new_entry.enhanced_image_search.text == 'true')
        self.assertTrue(new_entry.verified.text == 'false')

    def testConvertActualData(self):
        feed = webmastertools.SitesFeedFromString(test_data.SITES_FEED)
        self.assertTrue(len(feed.entry) == 1)
        entry = feed.entry[0]
        self.assertTrue(isinstance(entry, webmastertools.SitesEntry))
        self.assertTrue(entry.indexed.text == 'true')
        self.assertTrue(entry.crawled.text == '2008-09-14T08:59:28.000')
        self.assertTrue(entry.geolocation.text == 'US')
        self.assertTrue(entry.preferred_domain.text == 'none')
        self.assertTrue(entry.crawl_rate.text == 'normal')
        self.assertTrue(entry.enhanced_image_search.text == 'true')
        self.assertTrue(entry.verified.text == 'false')


class SitesFeedTest(unittest.TestCase):
    def setUp(self):
        self.feed = gdata.webmastertools.SitesFeedFromString(test_data.SITES_FEED)

    def testToAndFromString(self):
        self.assertTrue(len(self.feed.entry) == 1)
        for entry in self.feed.entry:
            self.assertTrue(isinstance(entry, webmastertools.SitesEntry))
        new_feed = webmastertools.SitesFeedFromString(self.feed.ToString())
        self.assertTrue(len(new_feed.entry) == 1)
        for entry in new_feed.entry:
            self.assertTrue(isinstance(entry, webmastertools.SitesEntry))


class SitemapsEntryTest(unittest.TestCase):
    def testRegularToAndFromString(self):
        entry = webmastertools.SitemapsEntry(
            sitemap_type=webmastertools.SitemapType(text='WEB'),
            sitemap_status=webmastertools.SitemapStatus(text='Pending'),
            sitemap_last_downloaded=webmastertools.SitemapLastDownloaded(
                text='2006-11-18T19:27:32.543Z'),
            sitemap_url_count=webmastertools.SitemapUrlCount(text='102'),
        )
        self.assertTrue(entry.sitemap_type.text == 'WEB')
        self.assertTrue(entry.sitemap_status.text == 'Pending')
        self.assertTrue(entry.sitemap_last_downloaded.text == \
                        '2006-11-18T19:27:32.543Z')
        self.assertTrue(entry.sitemap_url_count.text == '102')
        new_entry = webmastertools.SitemapsEntryFromString(entry.ToString())
        self.assertTrue(new_entry.sitemap_type.text == 'WEB')
        self.assertTrue(new_entry.sitemap_status.text == 'Pending')
        self.assertTrue(new_entry.sitemap_last_downloaded.text == \
                        '2006-11-18T19:27:32.543Z')
        self.assertTrue(new_entry.sitemap_url_count.text == '102')

    def testConvertActualData(self):
        feed = gdata.webmastertools.SitemapsFeedFromString(test_data.SITEMAPS_FEED)
        self.assertTrue(len(feed.entry) == 3)
        for entry in feed.entry:
            self.assertTrue(entry, webmastertools.SitemapsEntry)
            self.assertTrue(entry.sitemap_status, webmastertools.SitemapStatus)
            self.assertTrue(entry.sitemap_last_downloaded,
                            webmastertools.SitemapLastDownloaded)
            self.assertTrue(entry.sitemap_url_count, webmastertools.SitemapUrlCount)
            self.assertTrue(entry.sitemap_status.text == 'StatusValue')
            self.assertTrue(entry.sitemap_last_downloaded.text == \
                            '2006-11-18T19:27:32.543Z')
            self.assertTrue(entry.sitemap_url_count.text == '102')
            if entry.id.text == 'http://www.example.com/sitemap-index.xml':
                self.assertTrue(entry.sitemap_type, webmastertools.SitemapType)
                self.assertTrue(entry.sitemap_type.text == 'WEB')
                self.assertTrue(entry.sitemap_mobile_markup_language is None)
                self.assertTrue(entry.sitemap_news_publication_label is None)
            elif entry.id.text == 'http://www.example.com/mobile/sitemap-index.xml':
                self.assertTrue(entry.sitemap_mobile_markup_language,
                                webmastertools.SitemapMobileMarkupLanguage)
                self.assertTrue(entry.sitemap_mobile_markup_language.text == 'HTML')
                self.assertTrue(entry.sitemap_type is None)
                self.assertTrue(entry.sitemap_news_publication_label is None)
            elif entry.id.text == 'http://www.example.com/news/sitemap-index.xml':
                self.assertTrue(entry.sitemap_news_publication_label,
                                webmastertools.SitemapNewsPublicationLabel)
                self.assertTrue(entry.sitemap_news_publication_label.text == 'LabelValue')
                self.assertTrue(entry.sitemap_type is None)
                self.assertTrue(entry.sitemap_mobile_markup_language is None)


class SitemapsFeedTest(unittest.TestCase):
    def setUp(self):
        self.feed = gdata.webmastertools.SitemapsFeedFromString(
            test_data.SITEMAPS_FEED)

    def testToAndFromString(self):
        self.assertTrue(len(self.feed.entry) == 3)
        for entry in self.feed.entry:
            self.assertTrue(isinstance(entry, webmastertools.SitemapsEntry))
        new_feed = webmastertools.SitemapsFeedFromString(self.feed.ToString())
        self.assertTrue(len(new_feed.entry) == 3)
        for entry in new_feed.entry:
            self.assertTrue(isinstance(entry, webmastertools.SitemapsEntry))


if __name__ == '__main__':
    unittest.main()
