import os

from news_lk2.core import AbstractNewsPaper


class LankadeepaLk(AbstractNewsPaper):
    @classmethod
    def get_original_lang(cls):
        return 'si'

    @classmethod
    def get_index_urls(cls):
        return [
            'https://www.lankadeepa.lk/latest_news/1',
            'https://www.lankadeepa.lk/feature/2',
            'https://www.lankadeepa.lk/politics/13',
            'https://www.lankadeepa.lk/editorial/117',
        ]

    @classmethod
    def parse_article_urls(cls, soup):
        article_urls = []
        for h3 in soup.find_all('h3', {'class': 'mtbfive'}):
            article_url = h3.find('a').get('href')
            article_urls.append(article_url)
        return article_urls

    @classmethod
    def parse_title(cls, soup):
        h1 = soup.find('h1', {'class': 'post-title'})
        return h1.text

    @classmethod
    def parse_body_lines(cls, soup):
        header_inner = soup.find('header', {'class': 'post-content'})
        return list(
            map(
                lambda line: line.strip(),
                header_inner.text.strip().split('\n'),
            )
        )

    @classmethod
    def get_test_article_url(cls):
        return os.path.join(
            "https://www.lankadeepa.lk",
            "news",
            "%E0%B6%87%E0%B6%AD%E0%B7%8A%E0%B6%AF%E0%B7%85-%E0%B7%83%E0%B6%B8%E0%B6%9C-%E0%B6%85%E0%B6%BA%E0%B7%99%E0%B6%9A%E0%B7%8A-%E0%B7%83%E0%B7%90%E0%B6%9A%E0%B6%B4%E0%B7%92%E0%B6%A7/101-615339",  # noqa: E501,
        )


if __name__ == '__main__':
    LankadeepaLk.scrape()
