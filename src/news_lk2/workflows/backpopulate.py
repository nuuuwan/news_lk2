import argparse

from utils import timex

from news_lk2._utils import log
from news_lk2.analysis import paper
from news_lk2.core import Article
from news_lk2.core.filesys import git_checkout


def main(time_window, is_test_mode=False):
    log.debug(f'{time_window=}, {is_test_mode=}')

    git_checkout(force=not is_test_mode)
    article_files = paper.get_article_files()
    n = len(article_files)
    log.info(f'Backpopulating on {n} articles...')

    current_ut = timex.get_unixtime()
    i_within_time_window = 0
    for i, article_file in enumerate(article_files):
        d = Article.load_d_from_file(article_file)
        delta = current_ut - d['time_ut']
        if delta > time_window:
            continue

        i_within_time_window += 1
        article = Article.load_from_file(article_file)
        log.debug(f'{i +  1}/{n} {article.url} done.')
        article.store()

        if is_test_mode:
            if i_within_time_window > 5:
                break

    log.info(f'Backpopulated {i_within_time_window}/{n} articles.')


def get_options():
    parser = argparse.ArgumentParser()
    parser.add_argument('--time_window', type=int)
    return parser.parse_args()


if __name__ == '__main__':
    options = get_options()
    main(
        time_window=options.time_window,
        is_test_mode=False,
    )
