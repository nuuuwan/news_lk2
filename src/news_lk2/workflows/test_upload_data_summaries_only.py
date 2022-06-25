import random

from news_lk2._utils import log
from news_lk2.core.filesys import git_checkout
from news_lk2.custom_newspapers import newspaper_class_list
from news_lk2.workflows import common

DELIM_MD = '\n' * 2
MAX_ARTICLES_TO_UPLOAD = 200


def main():
    git_checkout(force=False)

    common.build_readme_summary()
    common.build_articles_summary()


if __name__ == '__main__':
    main()
