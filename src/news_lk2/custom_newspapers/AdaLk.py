import os

from news_lk2.core import AbstractNewsPaper


class AdaLk(AbstractNewsPaper):
    @classmethod
    def get_original_lang(cls):
        return 'si'

    @classmethod
    def get_index_urls(cls):
        return [
            'https://www.ada.lk/latest-news/11',
            'https://www.ada.lk/technology/5',
            'https://www.ada.lk/business/7',
        ]

    @classmethod
    def parse_article_urls(cls, soup):
        article_urls = []
        for div in soup.find_all('div', {'class': 'cat-detail-1'}):
            article_url = div.find('a').get('href')
            article_urls.append(article_url)
        return article_urls

    @classmethod
    def parse_title(cls, soup):
        h1 = soup.find('h1', {'class': 'single-head'})
        return h1.text

    @classmethod
    def parse_body_lines(cls, soup):
        div_body = soup.find('div', {'class': 'single-body-wrap'})
        return list(
            map(
                lambda line: line.strip(),
                div_body.text.strip().split('\n'),
            )
        )

    @classmethod
    def get_test_article_url(cls):
        return os.path.join(
            "https://www.ada.lk",
            "business",
            "%E0%B7%81%E0%B7%8A%E2%80%8D%E0%B6%BB%E0%B7%93-%E0%B6%BD%E0%B6%82%E0%B6%9A%E0%B7%8F-%E0%B6%B6%E0%B7%90%E0%B6%B3%E0%B7%94%E0%B6%B8%E0%B7%8A%E0%B6%9A%E0%B6%BB-%E0%B7%84%E0%B7%92%E0%B6%B8%E0%B7%92%E0%B6%BA%E0%B7%99%E0%B6%9A%E0%B7%94-%E0%B6%87%E0%B6%B8%E0%B7%99%E0%B6%BB%E0%B7%92%E0%B6%9A%E0%B7%8F%E0%B7%80%E0%B7%9A%E0%B6%AF%E0%B7%93-%E0%B6%B1%E0%B6%A9%E0%B7%94-%E0%B6%B4%E0%B7%80%E0%B6%BB%E0%B6%BD%E0%B7%8F/7-394679",  # noqa: E501,
        )


if __name__ == '__main__':
    for article in AdaLk.scrape():
        print(article.title)
