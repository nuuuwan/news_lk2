import os

from utils import timex

from news_lk2.core import AbstractNewsPaper

TIME_RAW_FORMAT = '%d %B %Y, %I:%M %p'


class DBSJeyarajCom(AbstractNewsPaper):
    @classmethod
    def use_selenium(cls):
        return False

    @classmethod
    def get_index_urls(cls):
        return [
            'https://dbsjeyaraj.com',
        ]

    @classmethod
    def parse_title(cls, soup):
        h1_title = soup.find('h1', {'class': 'entry-title'})
        return h1_title.text

    @classmethod
    def parse_author(cls, soup):
        span_author = soup.find('span', {'class': 'author vcard'})
        return span_author.text

    @classmethod
    def parse_article_urls(cls, soup):
        article_urls = []
        for h1_title in soup.find_all('h1', {'class': 'entry-title'}):
            article_url = h1_title.find('a').get('href')
            article_urls.append(article_url)
        return article_urls

    @classmethod
    def parse_time_ut(cls, soup):
        time_date = soup.find('time', {'class': 'entry-date'})
        s = time_date.text
        return timex.parse_time(
            s,
            TIME_RAW_FORMAT,
            timex.TIMEZONE_OFFSET_LK,
        )

    @classmethod
    def parse_body_lines(cls, soup):
        body_content = soup.find('div', {'class': 'entry-content'})
        return list(
            map(
                lambda line: line.strip(),
                body_content.text.strip().split('\n'),
            )
        )

    @classmethod
    def get_test_article_url(cls):
        return os.path.join(
            "https://dbsjeyaraj.com/dbsj/archives/78103",
        )
