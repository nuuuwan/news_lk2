import os
import re

from utils import timex

from news_lk2.core import AbstractNewsPaper

TIME_RAW_FORMAT = '%B %d, %Y %I:%M %p'


class AdaDeranaSinhalaLk(AbstractNewsPaper):
    @classmethod
    def use_selenium(cls):
        return True

    @classmethod
    def get_original_lang(cls):
        return 'si'

    @classmethod
    def get_index_urls(cls):
        return [
            'http://sinhala.adaderana.lk/sinhala-hot-news.php',
        ]

    @classmethod
    def parse_article_urls(cls, soup):
        article_urls = []
        for div in soup.find_all('div', {'class': 'news-story'}):
            article_url = div.find('a').get('href')
            article_urls.append(article_url)
        return article_urls

    @classmethod
    def parse_time_ut(cls, soup):
        span_time = soup.find('p', {'class': 'news-datestamp'})
        s = span_time.text.strip()
        s = re.sub(r'\s+', ' ', s)
        return timex.parse_time(
            s,
            TIME_RAW_FORMAT,
            timex.TIMEZONE_OFFSET_LK,
        )

    @classmethod
    def parse_title(cls, soup):
        article = soup.find('article', {'class': "news"})
        h1 = article.find('h1')
        return h1.text

    @classmethod
    def parse_body_lines(cls, soup):
        header_inner = soup.find('div', {'class': 'news-content'})
        return list(
            map(
                lambda line: line.strip(),
                header_inner.text.strip().split('\n'),
            )
        )

    @classmethod
    def get_test_article_url(cls):
        return os.path.join(
            "http://sinhala.adaderana.lk",
            "news/169446",
            "%E0%B6%9A%E0%B7%8F%E0%B6%B1%E0%B7%8A%E0%B6%AD%E0%B7%8F%E0%B7%80%E0%B6%B1%E0%B7%8A-%E0%B6%B6%E0%B7%92%E0%B6%BA%E0%B6%9C%E0%B6%B1%E0%B7%8A%E0%B7%80%E0%B7%8F-%E0%B6%9A%E0%B7%9C%E0%B6%BD%E0%B7%8A%E0%B6%BD%E0%B6%9A%E0%B7%91%E0%B6%B8%E0%B7%8A-%E0%B6%9A%E0%B7%85-%E0%B6%9A%E0%B6%BD%E0%B7%8A%E0%B6%BD%E0%B7%92%E0%B6%BA",  # noqa: E501
        )


if __name__ == '__main__':
    print(
        AdaDeranaSinhalaLk.parse_article(
            AdaDeranaSinhalaLk.get_test_article_url()
        )
    )
