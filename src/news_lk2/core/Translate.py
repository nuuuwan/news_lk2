import spacy
from deep_translator import GoogleTranslator
from utils.cache import cache

ENTS_LANG = 'en'
LANG_LIST = ['en', 'si', 'ta']
SPACY_NLP = spacy.load("en_core_web_sm")


def extract_named_entities(phrase):
    doc = SPACY_NLP(phrase)
    ents = []
    for ent in doc.ents:
        ents.append(dict(text=ent.text, label=ent.label_))
    return ents


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
    if word.isnumeric():
        return word

    word = word.strip()
    if len(word) < 1:
        return word

    if source_lang == target_lang:
        return word

    if len(word) > MAX_WORD_LEN:
        word = word[:MAX_WORD_LEN]

    return TRANSLATOR_IDX[source_lang][target_lang].translate(word)


def translate_ents(target_lang, ents):
    translated_ents = []
    for ent in ents:
        translated_ents.append(
            dict(
                text=translate(ENTS_LANG, target_lang, ent['text']),
                label=ent['label'],
            )
        )
    return translated_ents


def build_text_idx(
    source_lang,
    original_title,
    original_body_lines,
    original_author,
):
    text_idx = {}
    for target_lang in LANG_LIST:

        text_idx[target_lang] = dict(
            title=translate(source_lang, target_lang, original_title),
            author=translate(source_lang, target_lang, original_author),
            body_lines=list(
                map(
                    lambda line: translate(source_lang, target_lang, line),
                    original_body_lines,
                )
            ),
        )

    text_idx[ENTS_LANG]['title_ents'] = extract_named_entities(
        text_idx[ENTS_LANG]['title']
    )
    text_idx[ENTS_LANG]['body_line_ents_list'] = list(
        map(
            extract_named_entities,
            text_idx[ENTS_LANG]['body_lines'],
        )
    )

    for target_lang in LANG_LIST[1:]:
        text_idx[target_lang]['title_ents'] = translate_ents(
            target_lang,
            text_idx[ENTS_LANG]['title_ents'],
        )
        text_idx[target_lang]['body_line_ents_list'] = list(
            map(
                lambda ents: translate_ents(
                    target_lang,
                    ents,
                ),
                text_idx[ENTS_LANG]['body_line_ents_list'],
            )
        )

    return text_idx
