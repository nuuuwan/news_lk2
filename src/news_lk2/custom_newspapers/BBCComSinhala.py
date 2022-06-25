import os

from utils import timex

from news_lk2.core import AbstractNewsPaper

TIME_RAW_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'


class BBCComSinhala(AbstractNewsPaper):
    @classmethod
    def get_original_lang(cls):
        return 'si'

    @classmethod
    def get_index_urls(cls):
        return [
            'https://www.bbc.com/sinhala/topics/cg7267dz901t',
        ]

    @classmethod
    def parse_article_urls(cls, soup):
        article_urls = []
        for a in soup.find_all('a', {'class': 'emimjbx0'}):
            article_url = a.get('href')
            article_urls.append(article_url)
        return article_urls

    @classmethod
    def parse_time_ut(cls, soup):
        meta_published_time = soup.find(
            'meta', {'name': 'article:published_time'}
        )
        return timex.parse_time(
            meta_published_time.get('content'),
            TIME_RAW_FORMAT,
            timex.TIMEZONE_OFFSET_LK,
        )

    @classmethod
    def parse_title(cls, soup):
        h1 = soup.find('h1', {'id': 'content'})
        return h1.text

    @classmethod
    def parse_body_lines(cls, soup):
        divs = soup.find_all('div', {'class': 'bbc-19j92fr essoxwk0'})
        return list(
            map(
                lambda div: div.text,
                divs,
            )
        )

    @classmethod
    def get_test_article_url(cls):
        return os.path.join(
            "https://www.bbc.com/sinhala/sri-lanka-61923325",
        )


if __name__ == '__main__':
    BBCComSinhala.scrape()
