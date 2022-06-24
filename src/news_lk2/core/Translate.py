from deep_translator import GoogleTranslator
from utils.cache import cache

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
MAX_WORD_LEN = 2000


@cache('news_lk2.translate', 86400 * 1000)
def translate(source_lang, target_lang, word):
    word = word.strip()
    if len(word) < 1:
        return word

    if source_lang == target_lang:
        return word

    if len(word) > MAX_WORD_LEN:
        word = word[:MAX_WORD_LEN]

    return TRANSLATOR_IDX[source_lang][target_lang].translate(word)


def build_text_idx(source_lang, original_title, original_body_lines):
    text_idx = {}
    for target_lang in LANG_LIST:
        text_idx[target_lang] = dict(
            title=translate(source_lang, target_lang, original_title),
            body_lines=list(
                map(
                    lambda line: translate(source_lang, target_lang, line),
                    original_body_lines,
                )
            ),
        )
    return text_idx
