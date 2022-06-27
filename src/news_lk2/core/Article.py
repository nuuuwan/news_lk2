from utils import JSONFile, timex

from news_lk2._constants import WORDS_PER_MINUTE
from news_lk2._utils import log
from news_lk2.core.filesys import get_article_file, get_article_files

MINUTES_PER_TRUNCATED_BODY = 1
MAX_WORDS_TRUNCATED = WORDS_PER_MINUTE * MINUTES_PER_TRUNCATED_BODY


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

    def __str__(self):
        return '\n'.join(
            [
                self.newspaper_id,
                self.url,
                timex.format_time(self.time_ut),
                self.original_lang,
                self.original_title,
                '\n'.join(
                    self.text_idx[self.original_lang]['body_lines'],
                ),
            ]
        )

    @staticmethod
    def load_articles():
        articles = list(
            map(
                Article.load_from_file,
                get_article_files(),
            )
        )
        deduped_articles = list(
            dict(
                list(
                    map(
                        lambda article: [article.original_title, article],
                        articles,
                    )
                )
            ).values()
        )
        return list(reversed(sorted(deduped_articles)))
