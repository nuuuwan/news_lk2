import unittest

from news_lk2.custom_newspapers import newspaper_class_list


class TestCase(unittest.TestCase):
    @unittest.skip("Not implemented")
    def testParseAndStore(self):
        for newspaper_class in newspaper_class_list:
            article_url = newspaper_class.get_test_article_url()
            article = newspaper_class.parse_and_store_article(article_url)
            self.assertIsNotNone(article)


if __name__ == '__main__':
    unittest.main()
