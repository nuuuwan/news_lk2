import os

from utils import timex

from news_lk2.core import AbstractNewsPaper

TIME_RAW_FORMAT = '%Y-%m-%dT%H:%M:%S%z'


class ColomboTelegraphCom(AbstractNewsPaper):
    @classmethod
    def get_index_urls(cls):
        return [
            'https://www.colombotelegraph.com/index.php/category/news/',
            'https://www.colombotelegraph.com/index.php/category/editorial/',
        ]

    @classmethod
    def parse_article_urls(cls, soup):
        article_urls = []
        for h3 in soup.find_all(
            'h3', {'class': 'entry-title eltd-post-title'}
        ):
            article_url = h3.find('a').get('href')
            article_urls.append(article_url)
        return article_urls

    @classmethod
    def parse_time_ut(cls, soup):
        meta_published_time = soup.find(
            'meta', {'property': 'article:published_time'}
        )
        return timex.parse_time(
            meta_published_time.get('content'),
            TIME_RAW_FORMAT,
            timex.TIMEZONE_OFFSET_LK,
        )

    @classmethod
    def parse_title(cls, soup):
        h1_title = soup.find('h1', {'class': 'entry-title eltd-post-title'})
        return h1_title.text.strip()

    @classmethod
    def parse_author(cls, soup):
        a_author = soup.find('a', {'itemprop': 'author'})
        return a_author.text.replace('author:', '')

    @classmethod
    def parse_body_lines(cls, soup):
        div = soup.find('div', {'class': 'pf-content'})
        return list(
            map(
                lambda line: line.strip(),
                div.text.strip().split('\n'),
            )
        )

    @classmethod
    def get_test_article_url(cls):
        return os.path.join(
            "https://www.colombotelegraph.com",
            "index.php/preventing-crooks-from-entering-the-parliament/",
        )


if __name__ == '__main__':
    for article in ColomboTelegraphCom.scrape():
        print(article)
