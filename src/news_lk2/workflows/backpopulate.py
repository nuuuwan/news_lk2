from news_lk2._utils import log
from news_lk2.analysis.paper import get_articles
from news_lk2.core.filesys import git_checkout

MAX_ARTICLES_TO_TRANSLATE = 40


def main(is_test_mode=False):
    log.debug(f'{is_test_mode=}')

    git_checkout(force=not is_test_mode)
    articles = get_articles()
    n_articles = len(articles)
    log.debug(f'Backpopulating on {n_articles} articles...')

    for article in articles:
        log.debug(f'(Re)Storing {article.url}')
        article.store()

    log.debug(f'Backpopulated {n_articles} articles.')


if __name__ == '__main__':
    main(is_test_mode=False)
