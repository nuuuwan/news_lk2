import os
import shutil

import imageio
import matplotlib.pyplot as plt
from utils import timex
from wordcloud import WordCloud

from news_lk2._utils import log
from news_lk2.core.filesys import DIR_REPO

DIR_WORDCLOUDS = os.path.join(DIR_REPO, 'wordclouds')


def build_wordcloud(group_to_n):
    wordcloud = WordCloud(
        width=1600,
        height=900,
        background_color='white',
        random_state=1,
    ).generate_from_frequencies(group_to_n)

    plt.figure(figsize=(16, 9), facecolor=None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)

    wordcloud_file = os.path.join(DIR_REPO, 'wordcloud.png')
    plt.savefig(wordcloud_file)
    log.info(f'Saved wordcloud to {wordcloud_file}')

    if not os.path.exists(DIR_WORDCLOUDS):
        os.mkdir(DIR_WORDCLOUDS)

    time_id = timex.get_time_id(timezone=timex.TIMEZONE_OFFSET_LK)
    history_wordcloud_file = os.path.join(
        DIR_WORDCLOUDS, f'wordcloud-{time_id}.png'
    )
    shutil.copyfile(wordcloud_file, history_wordcloud_file)
    log.info(f'Saved wordcloud to {history_wordcloud_file}')


def get_wordcloud_image_files():
    image_files = []
    for file_only in os.listdir(DIR_WORDCLOUDS):
        image_files.append(os.path.join(DIR_WORDCLOUDS, file_only))
    return sorted(image_files)


def build_wordcloud_animation():
    N_IMAGES = 10
    image_files = get_wordcloud_image_files()
    image_files = image_files[-N_IMAGES:]

    images = []
    for image_file in image_files:
        images.append(imageio.imread(image_file))

    wordcloud_animation_file = os.path.join(DIR_REPO, 'wordcloud.gif')
    imageio.mimsave(wordcloud_animation_file, images, duration=1)
    log.info(f'Saved wordcloud animation to {wordcloud_animation_file}')


if __name__ == '__main__':
    build_wordcloud_animation()
