from ftfy import fix_text
from html import unescape


def repair_html_entities(text):
    before = ''

    while text != before:
        before, text = text, unescape(text)

    return text


def repair_broken_unicode(text):
    return fix_text(text, normalization='NFKD')
