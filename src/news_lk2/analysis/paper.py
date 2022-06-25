from utils import timex

from news_lk2.core import Article
from news_lk2.core.filesys import get_article_files

DELIM_MD = '\n\n'


def get_articles(ut_min=None):
    articles = list(
        map(
            Article.load_from_file,
            get_article_files(),
        )
    )
    if ut_min:
        articles = list(
            filter(
                lambda article: article.time_ut >= ut_min,
                articles,
            )
        )
    return list(reversed(sorted(articles)))


def get_date_id_to_articles(max_days_ago=None):
    if max_days_ago is not None:
        ut_limit = timex.get_unixtime() - timex.SECONDS_IN.DAY * max_days_ago
    else:
        ut_limit = None

    articles = get_articles()
    date_id_to_articles = {}
    for article in articles:
        if ut_limit and article.time_ut < ut_limit:
            continue
        date_id = article.date_id
        if date_id not in date_id_to_articles:
            date_id_to_articles[date_id] = []
        date_id_to_articles[date_id].append(article)

    date_id_to_articles = dict(
        sorted(
            list(
                map(
                    lambda item: [item[0], sorted(item[1])],
                    date_id_to_articles.items(),
                )
            ),
            key=lambda item: item[0],
        )
    )
    return date_id_to_articles
