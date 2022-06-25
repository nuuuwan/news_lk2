import os

from utils import File, JSONFile, timex

from news_lk2._utils import log
from news_lk2.core import Article
from news_lk2.core.filesys import DIR_REPO

DELIM_MD = '\n' * 2
N_LATEST = 100


def get_summary_stats(current_time):
    articles = Article.load_articles()
    summary_stats = {}
    for article in articles:
        time_ut = article.time_ut
        newspaper_id = article.newspaper_id
        article_age = current_time - time_ut
        for [time_window, label] in [
            [timex.SECONDS_IN.HOUR, 'Last Hour'],
            [timex.SECONDS_IN.HOUR * 3, 'Last 3 Hours'],
            [timex.SECONDS_IN.DAY, 'Last 24 Hours'],
            [timex.SECONDS_IN.WEEK, 'Last Week'],
            [None, 'Anytime'],
        ]:

            if time_window is None or article_age < time_window:
                if label not in summary_stats:
                    summary_stats[label] = {}
                if newspaper_id not in summary_stats[label]:
                    summary_stats[label][newspaper_id] = 0
                summary_stats[label][newspaper_id] += 1

    return summary_stats


def build_readme_summary():
    current_time = timex.get_unixtime()
    summary_stats = get_summary_stats(current_time)

    log.info('Building README.md')
    lines = []
    lines.append('# news_lk2 (upload_data summary)')
    time_last_run = timex.format_time(
        current_time, timezone=timex.TIMEZONE_OFFSET_LK
    )
    lines.append(f'*As of {time_last_run} (LK time)*')
    lines.append('')

    for label, summary_stats_for_label in summary_stats.items():
        total_n_articles = sum(list(summary_stats_for_label.values()))
        s = 's' if total_n_articles != 1 else ''
        lines.append(f'## {label} ({total_n_articles:,} Article{s})')
        total_n_articles = 0
        for newspaper_id, n_articles in sorted(
            summary_stats_for_label.items(),
            key=lambda x: -x[1],
        ):
            lines.append(f'* {n_articles:,}\t{newspaper_id}')

    readme_file = os.path.join(DIR_REPO, 'README.md')
    File(readme_file).write(DELIM_MD.join(lines))
    log.info(f'Wrote {readme_file}')


def build_articles_summary():
    log.info('Building articles.summary.json')
    articles = Article.load_articles()
    data_list = []
    for article in articles:
        # ArticleSummary = Article - "text_idx" + "file_name"
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
