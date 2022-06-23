from news_lk2 import common
from news_lk2._utils import log
from news_lk2.analysis.paper import get_articles
from news_lk2.core import TranslatedArticle
from news_lk2.core.filesys import git_checkout

MAX_ARTICLES_TO_TRANSLATE = 40


def main(is_test_mode=False):
    log.debug(f'{is_test_mode=}')
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
    common.build_readme_summary()
    common.build_articles_summary()


if __name__ == '__main__':
    main(is_test_mode=False)
