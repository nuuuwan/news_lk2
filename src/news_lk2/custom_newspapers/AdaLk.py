from utils import timex

from news_lk2.core import AbstractNewsPaper

TIME_RAW_FORMAT = '%Y-%m-%d %H:%M:%S'


class AdaLk(AbstractNewsPaper):
    @classmethod
    def get_original_lang(cls):
        return 'si'

    @classmethod
    def get_index_urls(cls):
        return [
            'https://www.ada.lk/latest-news/11',
        ]

    @classmethod
    def parse_article_urls(cls, soup):
        article_urls = []
        for div in soup.find_all('div', {'class': 'cat-detail-1'}):
            article_url = div.find('a').get('href')
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
        div_body = soup.find('div', {'class': 'single-body-wrap'})
        return list(
            map(
                lambda line: line.strip(),
                div_body.text.strip().split('\n'),
            )
        )


if __name__ == '__main__':
    AdaLk.scrape()
