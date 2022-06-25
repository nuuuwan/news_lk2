import os
from abc import ABC

from bs4 import BeautifulSoup
from utils import dt, mr, timex

from news_lk2._utils import log
from news_lk2.base.WWW import WWW
from news_lk2.core import Translate
from news_lk2.core.Article import Article
from news_lk2.core.filesys import get_article_file

MIN_ARTICLE_HTML_SIZE = 1_000
MIN_CHARS_IN_BODY_LINE = 60
MIN_WORDS_IN_BODY_LINE = 10
TIME_RAW_FORMAT = '%Y-%m-%d %H:%M:%S'


def is_valid_line(line):
    if len(line) < MIN_CHARS_IN_BODY_LINE:
        return False
    if len(line.split(' ')) < MIN_WORDS_IN_BODY_LINE:
        return False
    return True


def is_html_valid(html):
    if not html:
        log.warning('HTML is empty')
        return False

    if len(html) < MIN_ARTICLE_HTML_SIZE:
        log.warning('Insufficient HTML size')
        return False

    return True


class AbstractNewsPaper(ABC):
    @classmethod
    def use_selenium(cls):
        return False

    @classmethod
    def get_original_lang(cls):
        return Article.DEFAULT_ORIGINAL_LANG

    @classmethod
    def get_soup(cls, url):
        try:
            www = WWW(url)
            if cls.use_selenium():
                html = www.readSelenium()
            else:
                html = www.read()
        except Exception as e:
            log.error(str(e))
            return None

        if is_html_valid(html):
            return BeautifulSoup(html, 'html.parser')
        return None

    @classmethod
    def get_newspaper_id(cls):
        return dt.to_kebab(dt.camel_to_snake(cls.__name__))

    @classmethod
    def get_index_urls(cls):
        raise NotImplementedError

    @classmethod
    def parse_article_urls(cls, soup):
        raise NotImplementedError

    @classmethod
    def parse_time_ut(cls, soup):
        meta_time = soup.find('meta', {'itemprop': 'datePublished'})
        return timex.parse_time(
            meta_time.get('content').strip(),
            TIME_RAW_FORMAT,
            timex.TIMEZONE_OFFSET_LK,
        )

    @classmethod
    def parse_title(cls, soup):
        raise NotImplementedError

    @classmethod
    def parse_author(cls, soup):
        return "unknown"

    @classmethod
    def parse_body_lines(cls, soup):
        raise NotImplementedError

    @classmethod
    def get_article_urls(cls):
        article_urls = []
        for index_url in cls.get_index_urls():
            soup = cls.get_soup(index_url)
            if soup:
                article_urls += cls.parse_article_urls(soup)

        newspaper_id = cls.get_newspaper_id()
        log.info(f'Found {len(article_urls)} articles for {newspaper_id}')
        return article_urls

    @classmethod
    def get_test_article_url(cls):
        raise NotImplementedError

    @classmethod
    def parse_article(cls, article_url):
        soup = cls.get_soup(article_url)
        if not soup:
            raise Exception(f'{article_url} has invalid HTML. Not parsing.')

        original_lang = cls.get_original_lang()
        original_title = cls.parse_title(soup).strip()
        original_body_lines = list(
            filter(
                lambda line: is_valid_line(line),
                list(
                    map(
                        lambda line: line.strip(),
                        cls.parse_body_lines(soup),
                    )
                ),
            )
        )
        original_author = cls.parse_author(soup).strip()

        text_idx = Translate.build_text_idx(
            original_lang,
            original_title,
            original_body_lines,
            original_author,
        )

        article = Article(
            newspaper_id=cls.get_newspaper_id(),
            url=article_url,
            time_ut=cls.parse_time_ut(soup),
            original_lang=original_lang,
            original_title=original_title,
            text_idx=text_idx,
        )
        return article

    @classmethod
    def parse_and_store_article(cls, article_url):
        log.debug(f'[parse_and_store_article] {article_url}...')
        article_file = get_article_file(article_url)
        if os.path.exists(article_file):
            log.info(f'{article_file} already exists. Not parsing.')
            return None

        try:
            article = cls.parse_article(article_url)
            article.store()
            return article

        except Exception as e:
            log.error(str(e))
            return None

    @classmethod
    def scrape(cls):
        article_urls = cls.get_article_urls()

        def func_inner(article_url):
            article = cls.parse_and_store_article(article_url)
            return article

        article_list_raw = mr.map_parallel(
            func_inner,
            article_urls,
            max_threads=6,
        )

        article_list = list(
            filter(
                lambda article: article,
                article_list_raw,
            )
        )
        return article_list
