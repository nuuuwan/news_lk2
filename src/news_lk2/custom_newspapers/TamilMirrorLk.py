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
    def parse_author(cls, soup):
        return ""

    @classmethod
    def parse_body_lines(cls, soup):
        header_inner = soup.find('header', {'class': 'inner-content'})
        return list(
            map(
                lambda line: line.strip(),
                header_inner.text.strip().split('\n'),
            )
        )


if __name__ == '__main__':
    for article in TamilMirrorLk.scrape():
        print(article)
