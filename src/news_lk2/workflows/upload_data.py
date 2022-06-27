from news_lk2._utils import log
from news_lk2.core.articles_summary import build_articles_summary
from news_lk2.core.filesys import git_checkout
from news_lk2.core.readme import build_readme_summary
from news_lk2.core.trends import build_trending_summary
from news_lk2.core.upload_data import upload_data

DELIM_MD = '\n' * 2
MAX_ARTICLES_TO_UPLOAD = 200


def main(is_test_mode=False):
    log.debug(f'{is_test_mode=}')
    git_checkout(force=not is_test_mode)
    upload_data(is_test_mode)
    build_trending_summary()
    build_articles_summary()
    build_readme_summary()


if __name__ == '__main__':
    main(is_test_mode=False)
