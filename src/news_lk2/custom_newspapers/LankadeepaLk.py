from utils import timex

from news_lk2.core import AbstractNewsPaper

TIME_RAW_FORMAT = '%Y-%m-%d %H:%M:%S'


class LankadeepaLk(AbstractNewsPaper):
    @classmethod
    def get_original_lang(cls):
        return 'si'

    @classmethod
    def get_index_urls(cls):
        return [
            'https://www.lankadeepa.lk/latest_news/1',
        ]

    @classmethod
    def parse_article_urls(cls, soup):
        article_urls = []
        for h3 in soup.find_all('h3', {'class': 'mtbfive'}):
            article_url = h3.find('a').get('href')
            article_urls.append(article_url)
        return article_urls

    @classmethod
    def parse_time_ut(cls, soup):
        meta_time = soup.find('meta', {'itemprop': 'datePublished'})
        return timex.parse_time(
            meta_time.get('content').strip(),
            TIME_RAW_FORMAT,
            timex.TIMEZONE_OFFSET_LK,
        )

    @classmethod
    def parse_body_lines(cls, soup):
        header_inner = soup.find('header', {'class': 'post-content'})
        return list(
            map(
                lambda line: line.strip(),
                header_inner.text.strip().split('\n'),
            )
        )


if __name__ == '__main__':
    LankadeepaLk.scrape()
