from utils import timex

from news_lk2.core import AbstractNewsPaper

TIME_RAW_FORMAT = '%d %b, %Y\t| %I:%M %p'


class NewsFirstLk(AbstractNewsPaper):
    @classmethod
    def use_selenium(cls):
        return True

    @classmethod
    def get_index_urls(cls):
        return [
            'https://www.newsfirst.lk/latest-news/',
        ]

    @classmethod
    def parse_article_urls(cls, soup):
        article_urls = []
        for div in soup.find_all('div', {'class': 'desktop-news-block-ppd'}):
            article_url = div.find('a').get('href')
            article_urls.append(article_url)
        return article_urls

    @classmethod
    def parse_time_ut(cls, soup):
        span_time = soup.find('p', {'class': 'artical-new-byline'})
        s = span_time.text.strip()
        lines = s.split('\n')
        return timex.parse_time(
            lines[2],
            TIME_RAW_FORMAT,
            timex.TIMEZONE_OFFSET_LK,
        )

    @classmethod
    def parse_body_lines(cls, soup):
        header_inner = soup.find('div', {'class': 'thumb-para'})
        return list(
            map(
                lambda line: line.strip(),
                header_inner.text.strip().split('\n'),
            )
        )
