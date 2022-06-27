import os
import shutil

import matplotlib.pyplot as plt
from utils import timex
from wordcloud import WordCloud

from news_lk2._utils import log
from news_lk2.core.filesys import DIR_REPO


def build_wordcloud(group_to_n):
    wordcloud = WordCloud(
        width=1600,
        height=900,
        background_color='white',
        max_words=50,
    ).generate_from_frequencies(group_to_n)

    plt.figure(figsize=(16, 9), facecolor=None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)

    wordcloud_file = os.path.join(DIR_REPO, 'wordcloud.png')
    plt.savefig(wordcloud_file)
    log.info(f'Saved wordcloud to {wordcloud_file}')

    DIR_WORDCLOUDS = os.path.join(DIR_REPO, 'wordclouds')
    if not os.path.exists(DIR_WORDCLOUDS):
        os.mkdir(DIR_WORDCLOUDS)

    time_id = timex.get_time_id(timezone=timex.TIMEZONE_OFFSET_LK)
    history_wordcloud_file = os.path.join(
        DIR_WORDCLOUDS, f'wordcloud-{time_id}.png'
    )
    shutil.copyfile(wordcloud_file, history_wordcloud_file)
    log.info(f'Saved wordcloud to {history_wordcloud_file}')
