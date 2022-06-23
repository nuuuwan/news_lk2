from utils import timex

from news_lk2._constants import WORDS_PER_MINUTE
from news_lk2.core import Article
from news_lk2.core.filesys import get_article_files

DELIM_MD = '\n\n'


def get_articles(ut_min=None):
    articles = list(
        map(
            Article.load,
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


def get_articles_for_date_id(date_id):
    return list(
        filter(
            lambda article: article.date_id == date_id,
            get_articles(),
        )
    )


def get_date_ids():
    return sorted(
        list(
            set(
                map(
                    lambda article: article.date_id,
                    get_articles(),
                )
            )
        )
    )


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


def dedupe_by_title(articles):
    title_to_article = {}
    for article in articles:
        title_to_article[article.title] = article
    return sorted(list(title_to_article.values()))


def split_body_lines(lines, split_point=WORDS_PER_MINUTE):
    word_count = 0
    before_lines = []
    after_lines = []
    for line in lines:
        words = line.split(' ')
        if word_count < split_point:
            before_lines.append(line)
        else:
            after_lines.append(line)
        word_count += len(words)
    return before_lines, after_lines
