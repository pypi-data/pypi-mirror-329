import re
from unicodedata import normalize

ACCENT_GLYPHS = re.compile('[\u0060\u02C6\u02CA\u02CB\u02CE\u02CF\u02DD\u02DF\u02F4\u02F5\u02F6\u0300\u0301\u0302]+')


def remove_accent_glyphs(text):
    text = normalize('NFD', text)
    text = re.sub(ACCENT_GLYPHS, '', text)
    text = normalize('NFC', text)

    return text
