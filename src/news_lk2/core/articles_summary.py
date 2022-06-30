import os

from utils import JSONFile

from news_lk2._utils import log
from news_lk2.core.filesys import DIR_REPO
from news_lk2.core.trends import filter_articles, get_thing_ent_set

N_LATEST = 1_000


def get_article_summary(articles):
    articles_summary_idx = {}
    for article in articles:
        articles_summary_idx[article.original_title] = dict(
            newspaper_id=article.newspaper_id,
            url=article.url,
            time_ut=article.time_ut,
            original_lang=article.original_lang,
            original_title=article.original_title,
        )

    unsorted_articles_summary = list(articles_summary_idx.values())
    return sorted(
        unsorted_articles_summary,
        key=lambda x: -x['time_ut'],
    )


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


def get_group_to_articles(articles, ent_to_group):
    group_to_articles = {}
    recent_articles = filter_articles(articles)
    for article in recent_articles:
        file_name = article.file_name
        ent_set = get_thing_ent_set(article)
        for ent in ent_set:
            group = ent_to_group[ent]
            if group not in group_to_articles:
                group_to_articles[group] = []
            group_to_articles[group].append(file_name)
    return group_to_articles


def build_group_to_articles(articles, ent_to_group):
    group_to_articles = get_group_to_articles(articles, ent_to_group)
    group_to_articles_file = os.path.join(DIR_REPO, 'group_to_articles.json')
    JSONFile(group_to_articles_file).write(group_to_articles)
    log.info(f'Wrote {group_to_articles_file}')


def build_articles_summary(articles, ent_to_group):
    articles_summary = build_articles_summary_only(articles)
    build_articles_summary_latest(articles_summary)
    build_group_to_articles(articles, ent_to_group)
