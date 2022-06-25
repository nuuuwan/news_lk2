from news_lk2.core.filesys import git_checkout
from news_lk2.workflows import common

DELIM_MD = '\n' * 2
MAX_ARTICLES_TO_UPLOAD = 200


def main():
    git_checkout(force=False)

    common.build_all_summaries()


if __name__ == '__main__':
    main()
