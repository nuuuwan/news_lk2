

from news_lk2 import common
from news_lk2._utils import log
from news_lk2.core.filesys import git_checkout
from news_lk2.custom_newspapers import newspaper_class_list

DELIM_MD = '\n' * 2
N_LATEST = 100


def main(is_test_mode=False):
    log.debug(f'{is_test_mode=}')
    git_checkout()
    for newspaper_class in newspaper_class_list:
        log.debug(f'Scraping {newspaper_class.__name__}...')
        newspaper_class.scrape()
        if is_test_mode:
            break
    common.build_readme_summary()
    common.build_articles_summary()


if __name__ == '__main__':
    main(is_test_mode=False)
