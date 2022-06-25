import os

from utils import File, JSONFile, timex

from news_lk2._utils import log
from news_lk2.core import Article
from news_lk2.core.filesys import DIR_REPO

DELIM_MD = '\n' * 2
N_LATEST = 100
GITHUB_BASE = 'https://github.com/nuuuwan/news_lk2/blob/data'
TMP_BASE = '/tmp/news_lk2'


def group_by_time_and_newspaper(current_time):
    articles = Article.load_articles()
    idx = {}
    for article in articles:
        time_ut = article.time_ut
        newspaper_id = article.newspaper_id
        article_age = current_time - time_ut
        for [time_window, label] in [
            [timex.SECONDS_IN.MINUTE * 30, 'Last 30 Minutes'],
            [timex.SECONDS_IN.HOUR, 'Last Hour'],
            [timex.SECONDS_IN.HOUR * 3, 'Last 3 Hours'],
            [timex.SECONDS_IN.DAY, 'Last 24 Hours'],
            [timex.SECONDS_IN.WEEK, 'Last Week'],
            [None, 'All Time'],
        ]:

            if time_window is None or article_age < time_window:
                if label not in idx:
                    idx[label] = {}
                if newspaper_id not in idx[label]:
                    idx[label][newspaper_id] = []
                idx[label][newspaper_id].append(article)

    return idx


def build_readme_summary():
    current_time = timex.get_unixtime()
    idx = group_by_time_and_newspaper(current_time)

    log.info('Building README.md')
    lines = []
    lines.append('# Sri Lanka News App (Article Summary)')
    time_last_run = timex.format_time(
        current_time, timezone=timex.TIMEZONE_OFFSET_LK
    )
    lines.append(f'*As of {time_last_run} (LK time)*')
    lines.append('')

    for label, idx_for_label in idx.items():
        total_n_articles = sum(
            list(
                map(
                    lambda x: len(x[1]),
                    idx_for_label.items(),
                )
            )
        )
        lines.append(f'## {label} ({total_n_articles:,} Articles)')
        for newspaper_id, article_list in sorted(
            idx_for_label.items(),
            key=lambda x: -len(x[1]),
        ):
            n_articles = len(article_list)
            first_article = article_list[-1]
            url = first_article.file_name.replace(TMP_BASE, GITHUB_BASE)
            title = first_article.original_title
            lines.append(
                f'* **{n_articles:,}** {newspaper_id} ([{title}]({url}))',
            )

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
