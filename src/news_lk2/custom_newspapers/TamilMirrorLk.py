import os

from news_lk2.core import AbstractNewsPaper


class TamilMirrorLk(AbstractNewsPaper):
    @classmethod
    def get_original_lang(cls):
        return 'ta'

    @classmethod
    def get_index_urls(cls):
        return [
            'https://www.tamilmirror.lk/news/175',
        ]

    @classmethod
    def parse_article_urls(cls, soup):
        article_urls = []
        for div in soup.find_all('div', {'class': 'col-md-8'}):
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
            "https://www.tamilmirror.lk",
            "%E0%AE%9A%E0%AF%86%E0%AE%AF%E0%AF%8D%E0%AE%A4%E0%AE%BF%E0%AE%95%E0%AE%B3%E0%AF%8D/%E0%AE%AE%E0%AE%A9%E0%AF%8D%E0%AE%A9%E0%AE%BF%E0%AE%AA%E0%AF%8D%E0%AE%AA%E0%AF%81-%E0%AE%95%E0%AF%8B%E0%AE%B0%E0%AE%BF%E0%AE%A9%E0%AE%BE%E0%AE%B0%E0%AF%8D-%E0%AE%95%E0%AE%9E%E0%AF%8D%E0%AE%9A%E0%AE%A9/175-299164",  # noqa: E501
        )


if __name__ == '__main__':
    for article in TamilMirrorLk.scrape():
        print(article)
