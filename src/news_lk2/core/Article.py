from utils import JSONFile, timex

from news_lk2._constants import WORDS_PER_MINUTE
from news_lk2._utils import log
from news_lk2.core.filesys import get_article_file, get_article_files

MINUTES_PER_TRUNCATED_BODY = 1
MAX_WORDS_TRUNCATED = WORDS_PER_MINUTE * MINUTES_PER_TRUNCATED_BODY

newspaper_id_to_lang = {
    'ada-derana-lk': 'en',
    'ada-lk': 'si',
    'colombo-telegraph-com': 'en',
    'daily-ft-lk': 'en',
    'daily-mirror-lk': 'en',
    'daily-news-lk': 'en',
    'd-b-s-jeyaraj-com': 'en',
    'economy-next-com': 'en',
    'island-lk': 'en',
    'lankadeepa-lk': 'si',
    'news-first-lk': 'en',
    'tamil-mirror-lk': 'ta',
    'virakesari-lk': 'ta',
}


class Article:
    DEFAULT_ORIGINAL_LANG = 'en'

    def __init__(
        self,
        newspaper_id,
        url,
        time_ut,
        original_lang,
        original_title,
        text_idx,
    ):
        self.newspaper_id = newspaper_id
        self.url = url
        self.time_ut = time_ut
        self.original_lang = original_lang
        self.original_title = original_title
        self.text_idx = text_idx

    @staticmethod
    def load_d_from_file(article_file):
        return JSONFile(article_file).read()

    @staticmethod
    def load_from_file(article_file):
        d = Article.load_d_from_file(article_file)
        return Article.from_dict(d)

    @staticmethod
    def load_from_file_with_backpopulate(article_file):
        d = Article.load_d_from_file(article_file)
        return Article.from_dict_with_backpopulate(d)

    @staticmethod
    def from_dict(d):
        return Article(
            newspaper_id=d['newspaper_id'],
            url=d['url'],
            time_ut=d['time_ut'],
            original_lang=d.get('original_lang'),
            original_title=d.get('original_title'),
            text_idx=d.get('text_idx'),
        )

    @property
    def to_dict(self):
        return dict(
            newspaper_id=self.newspaper_id,
            url=self.url,
            time_ut=self.time_ut,
            original_lang=self.original_lang,
            original_title=self.original_title,
            text_idx=self.text_idx,
        )

    def store(self):
        JSONFile(self.file_name).write(self.to_dict)
        log.debug(f'Wrote {self.file_name}')

    @property
    def file_name(self):
        return get_article_file(self.url)

    @property
    def date_id(self):
        return timex.get_date_id(self.time_ut, timex.TIMEZONE_OFFSET_LK)

    def __lt__(self, other):
        return self.time_ut < other.time_ut

    @staticmethod
    def load_articles():
        articles = list(
            map(
                Article.load_from_file,
                get_article_files(),
            )
        )
        return list(reversed(sorted(articles)))
