from utils import JSONFile, timex

from news_lk2._constants import WORDS_PER_MINUTE
from news_lk2._utils import log
from news_lk2.core import Translate
from news_lk2.core.filesys import get_article_file

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
    def load_from_file(article_file):
        d = JSONFile(article_file).read()
        return Article.from_dict(d)

    @staticmethod
    def from_dict(d):
        url = d['url']
        newspaper_id = d['newspaper_id']

        # legacy
        if 'original_lang' in d:
            original_lang = d['original_lang']
        else:
            original_lang = newspaper_id_to_lang.get(newspaper_id)
            if not original_lang:
                raise Exception(newspaper_id)

        if 'original_title' in d:
            original_title = d['original_title']
        else:
            original_title = d['title']

        if 'text_idx' in d:
            text_idx = d['text_idx']
        else:
            text_idx = None
            if 'translate' in d:
                translate = d['translate']
                if len(translate.keys()) == 3:
                    text_idx = translate

            if not text_idx:
                origin_body_lines = d['body_lines']
                log.warning(f'[{url}] Translating')
                text_idx = Translate.build_text_idx(
                    original_lang,
                    original_title,
                    origin_body_lines,
                )

        return Article(
            newspaper_id=newspaper_id,
            url=url,
            time_ut=d['time_ut'],
            original_lang=original_lang,
            original_title=original_title,
            text_idx=text_idx,
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
            # legacy - eventually delete
            title=self.original_title,
            body_lines=self.text_idx[self.original_lang]['body_lines'],
            translate=self.text_idx,
        )

    def store(self):
        JSONFile(self.file_name).write(self.to_dict)
        log.debug(f'Wrote {self.file_name}')

        JSONFile(self.file_name_legacy).write(self.to_dict)
        log.debug(f'Wrote [legacy] {self.file_name_legacy}')

    @property
    def file_name(self):
        return get_article_file(self.url)

    @property
    def file_name_legacy(self):
        return get_article_file(self.url, '.translated')

    @property
    def date_id(self):
        return timex.get_date_id(self.time_ut, timex.TIMEZONE_OFFSET_LK)

    def __lt__(self, other):
        return self.time_ut < other.time_ut
