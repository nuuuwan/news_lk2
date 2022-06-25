import os

from utils import timex

from news_lk2.core import AbstractNewsPaper

TIME_RAW_FORMAT = '%Y-%m-%dT%H:%M:%S+05:30'


class DivainaLk(AbstractNewsPaper):
    @classmethod
    def get_original_lang(cls):
        return 'si'

    @classmethod
    def get_index_urls(cls):
        return [
            'https://divaina.lk/category/vigasa-puwath/',
            'https://divaina.lk/category/pradeshiya-puvath/',
            'https://divaina.lk/category/visheshanga/',
        ]

    @classmethod
    def parse_article_urls(cls, soup):
        article_urls = []
        for h3 in soup.find_all(
            'h3', {'class': 'entry-title td-module-title'}
        ):
            article_url = h3.find('a').get('href')
            article_urls.append(article_url)

        return article_urls

    @classmethod
    def parse_time_ut(cls, soup):
        time_ = soup.find(
            'time', {'class': 'entry-date updated td-module-date'}
        )
        return timex.parse_time(
            time_.get('datetime').strip(),
            TIME_RAW_FORMAT,
            timex.TIMEZONE_OFFSET_LK,
        )

    @classmethod
    def parse_title(cls, soup):
        h1 = soup.find('h1', {'class': 'entry-title'})
        return h1.text

    @classmethod
    def parse_body_lines(cls, soup):
        div = soup.find('div', {'class': 'td-post-content tagdiv-type'})
        ps = div.find_all('p')
        return list(
            map(
                lambda p: p.text,
                ps,
            )
        )

    @classmethod
    def get_test_article_url(cls):
        return os.path.join(
            "https://divaina.lk",
            "%e0%b6%9c%e0%b6%9c%e0%b6%b1%e0%b7%8a-%e0%b6%b8%e0%b6%bd%e0%b7%92%e0%b6%9a%e0%b7%8a-%e0%b6%b1%e0%b7%99%e0%b7%80%e0%b7%99%e0%b6%ba%e0%b7%92-%e0%b6%b4%e0%b6%bd%e0%b7%8a%e0%b6%bd%e0%b7%80%e0%b7%92/",  # noqa: E501,
        )


if __name__ == '__main__':
    DivainaLk.scrape()
