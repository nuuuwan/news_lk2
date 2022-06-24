from news_lk2._utils import log
from news_lk2.analysis import paper
from news_lk2.core import Article
from news_lk2.core.filesys import git_checkout

MAX_ARTICLES_TO_TRANSLATE = 40


def main(is_test_mode=False):
    log.debug(f'{is_test_mode=}')

    git_checkout(force=not is_test_mode)
    article_files = paper.get_article_files()
    if is_test_mode:
        article_files = article_files[:10]

    n = len(article_files)
    log.debug(f'Backpopulating on {n} articles...')

    for i, article_file in enumerate(article_files):
        article = Article.load_from_file(article_file)
        log.info(f'{i +  1}/{n} {article.url} done.')
        article.store()

    log.debug(f'Backpopulated {n} articles.')


if __name__ == '__main__':
    main(is_test_mode=False)
