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
    def parse_author(cls, soup):
        return ""

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


if __name__ == '__main__':
    DivainaLk.scrape()
