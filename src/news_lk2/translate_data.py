from news_lk2.analysis.paper import get_articles
from news_lk2.core import TranslatedArticle
from news_lk2.core.filesys import git_checkout

MAX_ARTICLES_TO_TRANSLATE = 20


def main(is_test_mode=False):
    git_checkout()
    articles = get_articles()
    i_translated = 0
    for article in articles:
        translated_article = TranslatedArticle.initFromArticle(article)
        if not translated_article.store():
            continue

        i_translated += 1
        if i_translated >= MAX_ARTICLES_TO_TRANSLATE:
            break
        if is_test_mode:
            break


if __name__ == '__main__':
    main(is_test_mode=False)
