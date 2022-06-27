import os

from utils import JSONFile

from news_lk2._utils import log
from news_lk2.core import Article
from news_lk2.core.filesys import DIR_REPO

N_LATEST = 100


def build_articles_summary():
    log.info('Building articles.summary.json')
    articles = Article.load_articles()
    data_list = []
    for article in articles:
        data_list.append(
            dict(
                newspaper_id=article.newspaper_id,
                url=article.url,
                time_ut=article.time_ut,
                original_lang=article.original_lang,
                original_title=article.original_title,
                file_name=article.file_name,
            )
        )

    articles_summary_file = os.path.join(DIR_REPO, 'articles.summary.json')
    JSONFile(articles_summary_file).write(data_list)
    n_data_list = len(data_list)
    log.info(f'Wrote {n_data_list} articles to {articles_summary_file}')

    articles_summary_latest_file = os.path.join(
        DIR_REPO, 'articles.summary.latest.json'
    )
    latest_data_list = data_list[:N_LATEST]
    JSONFile(articles_summary_latest_file).write(latest_data_list)
    n_latest_data_list = len(latest_data_list)
    log.info(
        f'Wrote {n_latest_data_list} articles '
        + f'to {articles_summary_latest_file}',
    )
