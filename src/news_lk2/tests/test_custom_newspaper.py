import time
import unittest

from news_lk2.core.Translate import LANG_LIST
from news_lk2.custom_newspapers import (AdaDeranaLk, CeylonTodayLk,
                                        DailyNewsLk, DBSJeyarajCom, DivainaLk,
                                        IslandLk, newspaper_class_list)

MAX_ARTICLE_AGE = 86_400 * 1_000
MIN_ARTICLE_TITLE_LEN = 10
MAX_PARSE_ARTICLE_TIME = 120


UNSAFE_NEWSPAPER_CLASS_LIST = [
    AdaDeranaLk,
    CeylonTodayLk,
    DailyNewsLk,
    DBSJeyarajCom,
    DivainaLk,
    IslandLk,
]

SAFE_NEWSPAPER_CLASS_LIST = list(
    filter(
        lambda newspaper_class: newspaper_class
        not in UNSAFE_NEWSPAPER_CLASS_LIST,
        newspaper_class_list,
    )
)


def helper_test_parse(test_case, newspaper_class_list):
    for newspaper_class in newspaper_class_list:
        article_url = newspaper_class.get_test_article_url()

        time_start = time.time()
        article = newspaper_class.parse_article(article_url)
        delta_time = time.time() - time_start

        test_case.assertIsNotNone(article)
        # newspaper_id
        newspaper_id = newspaper_class.get_newspaper_id()
        test_case.assertEqual(newspaper_id, article.newspaper_id)
        # url
        test_case.assertEqual(article_url, article.url)
        # time_ut
        test_case.assertLess(article.time_ut, time_start)
        test_case.assertGreater(article.time_ut, time_start - MAX_ARTICLE_AGE)
        # original_lang
        test_case.assertEqual(
            newspaper_class.get_original_lang(), article.original_lang
        )
        # original_title
        test_case.assertGreater(
            len(article.original_title), MIN_ARTICLE_TITLE_LEN
        )
        # text_idx
        for lang in LANG_LIST:
            test_case.assertIn(lang, article.text_idx)
            lang_text_idx = article.text_idx[lang]
            test_case.assertIn('title', lang_text_idx)
            test_case.assertIn('body_lines', lang_text_idx)

        print(f'{delta_time:.1f}s\t{newspaper_id}')
        test_case.assertLess(
            delta_time,
            MAX_PARSE_ARTICLE_TIME,
            delta_time,
        )


class TestCase(unittest.TestCase):
    @unittest.skip("Known failures")
    def testParseSafe(self):
        helper_test_parse(self, SAFE_NEWSPAPER_CLASS_LIST)

    @unittest.skip("Known failures")
    def testParseUnsafeSafe(self):
        helper_test_parse(self, UNSAFE_NEWSPAPER_CLASS_LIST)


if __name__ == '__main__':
    unittest.main()
