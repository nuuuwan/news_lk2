import os

from utils import JSONFile

from news_lk2._utils import log
from news_lk2.core.filesys import DIR_REPO

N_LATEST = 400


def get_article_summary(articles):
    articles_summary = []
    for article in articles:
        articles_summary.append(
            dict(
                file_name=article.file_name,
            )
        )
    return articles_summary


def build_articles_summary_only(articles):
    articles_summary = get_article_summary(articles)
    articles_summary_file = os.path.join(DIR_REPO, 'articles.summary.json')
    JSONFile(articles_summary_file).write(articles_summary)
    n_articles_summary = len(articles_summary)
    log.info(
        f'Wrote {n_articles_summary} articles to {articles_summary_file}'
    )
    return articles_summary


def build_articles_summary_latest(articles_summary):
    articles_summary_latest_file = os.path.join(
        DIR_REPO, 'articles.summary.latest.json'
    )
    articles_summary_latest = articles_summary[:N_LATEST]
    JSONFile(articles_summary_latest_file).write(articles_summary_latest)
    n_articles_summary_latest = len(articles_summary_latest)
    log.info(
        f'Wrote {n_articles_summary_latest} articles '
        + f'to {articles_summary_latest_file}',
    )


def build_articles_summary(articles):
    articles_summary = build_articles_summary_only(articles)
    build_articles_summary_latest(articles_summary)


if __name__ == '__main__':
    build_articles_summary()
