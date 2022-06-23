import os

from deep_translator import GoogleTranslator
from utils import jsonx
from utils.cache import cache

from news_lk2._utils import log
from news_lk2.core.Article import Article
from news_lk2.core.filesys import get_article_file

LANG_LIST = ['si', 'ta', 'en']


def get_translator(source_lang, target_lang):
    return GoogleTranslator(source=source_lang, target=target_lang)


def get_translator_idx():
    idx = {}
    for source_lang in LANG_LIST:
        idx[source_lang] = {}
        for target_lang in LANG_LIST:
            if source_lang == target_lang:
                continue
            idx[source_lang][target_lang] = get_translator(
                source_lang, target_lang
            )
    return idx


TRANSLATOR_IDX = get_translator_idx()


@cache('news_lk2.translate', 86400 * 1000)
def translate(source_lang, target_lang, word):
    if source_lang == target_lang:
        return word
    return TRANSLATOR_IDX[source_lang][target_lang].translate(word)


class TranslatedArticle(Article):
    @staticmethod
    def initFromArticle(article):
        return TranslatedArticle(
            article.newspaper_id,
            article.url,
            article.time_ut,
            article.title,
            article.body_lines,
            article.original_lang,
        )

    def get_translated(self):
        translated = {}
        source_lang = self.original_lang
        for target_lang in LANG_LIST:
            translated[target_lang] = {
                'title': translate(source_lang, target_lang, self.title),
                'body_lines': list(
                    map(
                        lambda line: translate(
                            source_lang, target_lang, line
                        ),
                        self.body_lines,
                    )
                ),
            }
        return translated

    @property
    def dict(self):
        return dict(
            newspaper_id=self.newspaper_id,
            url=self.url,
            time_ut=self.time_ut,
            title=self.title,
            body_lines=self.body_lines,
            original_lang=self.original_lang,
            translate=self.get_translated(),
        )

    @property
    def file_name(self):
        return get_article_file(self.url, '.translated')

    def store(self):
        if os.path.exists(self.file_name):
            log.debug(f'{self.file_name} already exists. Not storing.')
            return False

        jsonx.write(self.file_name, self.dict)
        log.info(f'Wrote {self.file_name}')
        return True
