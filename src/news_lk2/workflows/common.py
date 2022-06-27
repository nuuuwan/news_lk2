from news_lk2.core.articles_summary import build_articles_summary
from news_lk2.core.readme import build_readme_summary
from news_lk2.core.trends import build_trending_summary


def build_all_summaries():
    build_trending_summary()
    build_articles_summary()
    build_readme_summary()
