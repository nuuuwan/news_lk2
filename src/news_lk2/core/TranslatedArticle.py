import os

from deep_translator import GoogleTranslator
from utils import jsonx
from utils.cache import cache

from news_lk2._utils import log
from news_lk2.core.Article import Article
from news_lk2.core.filesys import get_article_file

SOURCE_LANG = 'en'
TARGET_LANG_LIST = ['si', 'ta']


def get_translator(target_lang):
    return GoogleTranslator(source=SOURCE_LANG, target=target_lang)


translator_idx = dict(
    list(
        map(
            lambda target_lang: [target_lang, get_translator(target_lang)],
            TARGET_LANG_LIST,
        )
    )
)


@cache('news_lk2.translate', 86400 * 1000)
def translate(target_lang, word):
    translated_word = translator_idx[target_lang].translate(word)
    return translated_word


class TranslatedArticle(Article):
    @staticmethod
    def initFromArticle(article):
        return TranslatedArticle(
            article.newspaper_id,
            article.url,
            article.time_ut,
            article.title,
            article.body_lines,
        )

    def get_translated(self):
        translated = {}
        for target_lang in TARGET_LANG_LIST:
            translated[target_lang] = {
                'title': translate(target_lang, self.title),
                'body_lines': list(
                    map(
                        lambda line: translate(target_lang, line),
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
