import os

from fuzzywuzzy import fuzz
from utils import TSVFile, timex

from news_lk2._utils import log
from news_lk2.core import Article
from news_lk2.core.ents import THING_ENTS
from news_lk2.core.filesys import DIR_REPO
from news_lk2.core.wordcloud import build_wordcloud

DELIM_MD = '\n' * 2
N_LATEST = 100
GITHUB_BASE = 'https://github.com/nuuuwan/news_lk2/blob/data'
TMP_BASE = '/tmp/news_lk2'
DELIM = ':'
MAX_ARTICLE_AGE_FOR_TRENDS = timex.SECONDS_IN.WEEK
MIN_FUZZ_RATIO_FOR_GROUP = 85


def build_trending_summary():
    current_time = timex.get_unixtime()
    articles = Article.load_articles()
    ents = []
    for article in articles:
        time_ut = article.time_ut
        article_age = current_time - time_ut

        if article_age > MAX_ARTICLE_AGE_FOR_TRENDS:
            continue

        if (
            not article.text_idx
            or 'en' not in article.text_idx
            or 'title_ents' not in article.text_idx['en']
        ):
            continue
        text_idx = article.text_idx['en']
        ents += text_idx['title_ents']
        for ents0 in text_idx['body_line_ents_list']:
            ents += ents0

    ent_text_to_n = {}
    for ent in ents:
        if ent['label'] not in THING_ENTS:
            continue
        k = ent['text'].replace('the ', '').strip()

        if k not in ent_text_to_n:
            ent_text_to_n[k] = 0
        ent_text_to_n[k] += 1

    sorted_ent_and_n = sorted(
        ent_text_to_n.items(),
        key=lambda x: -x[1],
    )

    sorted_ents = list(
        map(
            lambda x: x[0],
            sorted_ent_and_n,
        )
    )

    ent_to_group = {}
    n = len(sorted_ents)
    for i in range(0, n):
        if sorted_ents[i] in ent_to_group:
            continue
        for j in range(0, i + 1):
            if (
                fuzz.ratio(sorted_ents[i], sorted_ents[j])
                > MIN_FUZZ_RATIO_FOR_GROUP
            ):
                ent_to_group[sorted_ents[i]] = sorted_ents[j]
                break

    group_to_n = {}
    for ent, n in sorted_ent_and_n:
        group = ent_to_group[ent]
        if group not in group_to_n:
            group_to_n[group] = 0
        group_to_n[group] += n

    sorted_group_and_n = sorted(
        group_to_n.items(),
        key=lambda x: -x[1],
    )

    data_list = list(
        map(
            lambda x: dict(
                ent_group=x[0],
                n=x[1],
            ),
            sorted_group_and_n,
        )
    )

    trending_file = os.path.join(DIR_REPO, 'trending.tsv')
    TSVFile(trending_file).write(data_list)
    n_data_list = len(data_list)
    log.info(f'Wrote {n_data_list} ents to {trending_file}')

    build_wordcloud(group_to_n)
