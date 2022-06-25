import os

from news_lk2.core import AbstractNewsPaper

TIME_RAW_FORMAT = '%A, %d %B %Y %H:%M'


class DailyFtLk(AbstractNewsPaper):
    @classmethod
    def get_index_urls(cls):
        return [
            'https://www.ft.lk/ft-news/56',
            'https://www.ft.lk/business-news/34',
            'https://www.ft.lk/opinion/14',
        ]

    @classmethod
    def parse_article_urls(cls, soup):
        article_urls = []
        for div in soup.find_all('div', {'class': 'col-md-6'}):
            article_url = div.find('a').get('href')
            article_urls.append(article_url)
        return article_urls

    @classmethod
    def parse_title(cls, soup):
        h1 = soup.find('h1', {'class': 'innerheader'})
        return h1.text

    @classmethod
    def parse_body_lines(cls, soup):
        header_inner = soup.find('header', {'class': 'inner-content'})
        return list(
            map(
                lambda line: line.strip(),
                header_inner.text.strip().split('\n'),
            )
        )

    @classmethod
    def get_test_article_url(cls):
        return os.path.join(
            "https://www.ft.lk",
            "business",
            "100-000-jobs-up-for-grabs-for-Lankans-in-Romania/34-736670",
        )
