import os

from utils import Git, hashx

from news_lk2._utils import log

REPO_NAME = 'news_lk2'
GIT_REPO_URL = f'https://github.com/nuuuwan/{REPO_NAME}.git'
DIR_ROOT = '/tmp'
DIR_REPO = os.path.join(DIR_ROOT, REPO_NAME)
DIR_ARTICLES = os.path.join(
    DIR_REPO,
    'articles',
)

SALT = '5568445278803347'
HASH_LENGTH = 8
IGNORE_LIST = ['.git', '.gitignore', '.DS_Store']
SHARD_NAME_LENGTH = 2
ARTICLE_FILE_ONLY_LEN = HASH_LENGTH + 5


def get_dir_article_shard(file_name_only, dir_prefix=''):
    assert len(file_name_only) == ARTICLE_FILE_ONLY_LEN
    dir_shard_only = file_name_only[:SHARD_NAME_LENGTH]
    return os.path.join(DIR_ARTICLES + dir_prefix, dir_shard_only)


def get_hash(url):
    return hashx.md5(url + SALT)[:HASH_LENGTH]


def get_article_file_only(url):
    h = get_hash(url)
    return f'{h}.json'


def get_article_file(url, dir_prefix=''):
    file_name_only = get_article_file_only(url)
    dir_article_shard = get_dir_article_shard(file_name_only, dir_prefix)
    if not os.path.exists(dir_article_shard):
        os.system(f'mkdir -p {dir_article_shard}')
    return os.path.join(dir_article_shard, file_name_only)


def git_checkout(force=True):
    log.debug(f'[git_checkout] {force=}')
    git = Git(GIT_REPO_URL)
    git.clone(DIR_REPO, force=force)
    git.checkout('data')
    log.debug(f'Cloned {GIT_REPO_URL} [data] to {DIR_REPO}')


def get_article_files():
    article_files = []
    for dir_article_shard_only in os.listdir(DIR_ARTICLES):
        dir_article_shard = os.path.join(DIR_ARTICLES, dir_article_shard_only)
        for article_file_only in os.listdir(dir_article_shard):
            article_file = os.path.join(dir_article_shard, article_file_only)
            article_files.append(article_file)
    return article_files
