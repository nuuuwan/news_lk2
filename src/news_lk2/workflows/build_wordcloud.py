import os
import random

import matplotlib.pyplot as plt
from utils import dt
from wordcloud import STOPWORDS, WordCloud

from news_lk2._utils import log
from news_lk2.core.filesys import DIR_REPO


def build_wordcloud(group_to_n):
    comment_words = []
    for group, n in group_to_n.items():
        if group[:4].lower() == 'the ':
            group = group[:4]
        group = dt.snake_to_camel(dt.to_snake(group))
        comment_words += [group for i in range(0, n)]
    random.shuffle(comment_words)
    comment_words = " ".join(comment_words)

    wordcloud = WordCloud(
        width=1600,
        height=900,
        background_color='white',
        stopwords=set(STOPWORDS),
        min_font_size=10,
    ).generate(comment_words)

    plt.figure(figsize=(16, 9), facecolor=None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)

    wordcloud_file = os.path.join(DIR_REPO, 'wordcloud.png')
    plt.savefig(wordcloud_file)
    log.info(f'Saved wordcloud to {wordcloud_file}')
