import os

from utils import timex

from news_lk2.core import AbstractNewsPaper

TIME_RAW_FORMAT = '%Y-%m-%d %H:%M:%S'


class VirakesariLk(AbstractNewsPaper):
    @classmethod
    def get_original_lang(cls):
        return 'ta'

    @classmethod
    def get_index_urls(cls):
        return [
            'https://www.virakesari.lk/category/local',
            'https://www.virakesari.lk/category/feature',
        ]

    @classmethod
    def parse_article_urls(cls, soup):
        article_urls = []
        for div in soup.find_all('div', {'class': 'media-body'}):
            article_url = div.find('a').get('href')
            article_urls.append(article_url)
        return article_urls

    @classmethod
    def parse_time_ut(cls, soup):
        article = soup.find('article')
        p_meta = article.find('p', {'class', 'meta'})
        return timex.parse_time(
            p_meta.text[-19:],
            TIME_RAW_FORMAT,
            timex.TIMEZONE_OFFSET_LK,
        )

    @classmethod
    def parse_title(cls, soup):
        article = soup.find('article')
        h1 = article.find('h1')
        return h1.text

    @classmethod
    def parse_author(cls, soup):
        article = soup.find('article')
        p_meta = article.find('p', {'class', 'meta'})
        return (
            p_meta.text[:-19]
            .replace('Published', '')
            .replace('by', '')
            .replace('on', '')
        )

    @classmethod
    def parse_body_lines(cls, soup):
        div = soup.find('div', {'class': 'post-content'})
        return list(
            map(
                lambda line: line.strip(),
                div.text.strip().split('\n'),
            )
        )

    @classmethod
    def get_test_article_url(cls):
        return os.path.join(
            "https://www.virakesari.lk/article/130122",
        )


if __name__ == '__main__':
    for article in VirakesariLk.scrape():
        print(article)
