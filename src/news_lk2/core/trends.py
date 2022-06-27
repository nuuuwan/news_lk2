import math
import os
import re

from fuzzywuzzy import fuzz
from utils import JSONFile, timex

from news_lk2._utils import log
from news_lk2.core.ents import THING_ENTS
from news_lk2.core.filesys import DIR_REPO

MIN_FUZZ_RATIO_FOR_GROUP = 85
HALF_LIFE_DAYS = 1


def sort_by_value(_dict):
    sorted_items = list(
        sorted(
            _dict.items(),
            key=lambda x: -x[1],
        )
    )
    return dict(sorted_items)


def filter_articles(articles):
    def filter_article(article):
        if (
            not article.text_idx
            or 'en' not in article.text_idx
            or 'title_ents' not in article.text_idx['en']
        ):
            return False

        return True

    filtered_articles = list(filter(filter_article, articles))
    n_filtered_articles = len(filtered_articles)
    log.debug(f'{n_filtered_articles=}')
    return filtered_articles


def get_thing_ent_set(article):
    text_idx = article.text_idx['en']
    ents = text_idx['title_ents']
    for ents0 in text_idx['body_line_ents_list']:
        ents += ents0

    def filter_thing_ent(ent):
        return ent['label'] in THING_ENTS

    def map_ent_text(ent):
        ent_text = ent['text']
        ent_text = ent_text.replace('.', "")
        ent_text = re.sub("the ", "", ent_text, flags=re.IGNORECASE)
        return ent_text

    return list(
        set(
            list(
                map(
                    map_ent_text,
                    list(
                        filter(
                            filter_thing_ent,
                            ents,
                        )
                    ),
                )
            )
        )
    )


def get_ent_to_n(articles):
    current_time = timex.get_unixtime()
    ent_to_n = {}
    for article in articles:
        time_ut = article.time_ut
        age_days = (current_time - time_ut) / timex.SECONDS_IN.DAY
        w = (
            1
            if age_days < 1
            else 1 / (math.pow(2, age_days / HALF_LIFE_DAYS))
        )

        ent_set = get_thing_ent_set(article)
        for ent in ent_set:
            if ent not in ent_to_n:
                ent_to_n[ent] = 0
            ent_to_n[ent] += w

    return sort_by_value(ent_to_n)


def get_group_to_n(ent_to_n):
    sorted_ents = list(ent_to_n.keys())

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
    for ent, n in ent_to_n.items():
        group = ent_to_group[ent]
        if group not in group_to_n:
            group_to_n[group] = 0
        group_to_n[group] += n

    return ent_to_group, sort_by_value(group_to_n)


def build_trending_summary(articles):
    recent_articles = filter_articles(articles)
    ent_to_n = get_ent_to_n(recent_articles)
    ent_to_n_file = os.path.join(DIR_REPO, 'ent_to_n.json')
    JSONFile(ent_to_n_file).write(ent_to_n)
    log.debug(f'Wrote {ent_to_n_file}')

    ent_to_group, group_to_n = get_group_to_n(ent_to_n)

    ent_to_group_file = os.path.join(DIR_REPO, 'ent_to_group.json')
    JSONFile(ent_to_group_file).write(ent_to_group)
    log.debug(f'Wrote {ent_to_group_file}')

    group_to_n_file = os.path.join(DIR_REPO, 'group_to_n.json')
    JSONFile(group_to_n_file).write(group_to_n)
    log.debug(f'Wrote {group_to_n_file}')

    return ent_to_group, group_to_n


if __name__ == '__main__':
    build_trending_summary()
