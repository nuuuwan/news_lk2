import time
import unittest

from news_lk2.core.Translate import LANG_LIST
from news_lk2.custom_newspapers import newspaper_class_list

MAX_ARTICLE_AGE = 86_400 * 1_000
MIN_ARTICLE_TITLE_LEN = 10
MAX_PARSE_ARTICLE_TIME = 120


class TestCase(unittest.TestCase):
    @unittest.skip("Known failures")
    def testParse(self):
        for newspaper_class in newspaper_class_list:
            article_url = newspaper_class.get_test_article_url()

            time_start = time.time()
            article = newspaper_class.parse_article(article_url)
            delta_time = time.time() - time_start

            self.assertIsNotNone(article)
            # newspaper_id
            newspaper_id = newspaper_class.get_newspaper_id()
            self.assertEqual(newspaper_id, article.newspaper_id)
            # url
            self.assertEqual(article_url, article.url)
            # time_ut
            self.assertLess(article.time_ut, time_start)
            self.assertGreater(article.time_ut, time_start - MAX_ARTICLE_AGE)
            # original_lang
            self.assertEqual(
                newspaper_class.get_original_lang(), article.original_lang
            )
            # original_title
            self.assertGreater(
                len(article.original_title), MIN_ARTICLE_TITLE_LEN
            )
            # text_idx
            for lang in LANG_LIST:
                self.assertIn(lang, article.text_idx)
                lang_text_idx = article.text_idx[lang]
                self.assertIn('title', lang_text_idx)
                self.assertIn('body_lines', lang_text_idx)

            print(f'{delta_time:.1f}s\t{newspaper_id}')
            self.assertLess(
                delta_time,
                MAX_PARSE_ARTICLE_TIME,
                delta_time,
            )


if __name__ == '__main__':
    unittest.main()
