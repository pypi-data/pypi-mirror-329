import markitdown
import re
import tempfile
import trafilatura
from bs4 import BeautifulSoup, Comment
from markdownify import MarkdownConverter
from nlpclean.table import table_span_normalize

_MEANINGLESS_TAGS = [
    'applet', 'audio', 'canvas', 'comment', 'datalist', 'embed', 'form',
    'frame', 'frameset', 'iframe', 'img', 'kbd', 'map', 'menu', 'noembed',
    'noframes', 'noscript', 'object', 'output', 'plaintext', 'script', 'style',
    'svg', 'template', 'title', 'video', 'xmp'
]

_BLOCKLEVEL_TAGS = [
    'address', 'article', 'aside', 'blockquote', 'center', 'dd', 'details',
    'dialog', 'dir', 'div', 'dl', 'dt', 'fieldset', 'figcaption', 'figure',
    'footer', 'form', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'header', 'hgroup',
    'hr', 'isindex', 'li', 'main', 'menu', 'nav', 'noframes', 'noscript', 'ol',
    'p', 'pre', 'section', 'table', 'td', 'th', 'tr', 'ul'
]


def html_to_article(html, parser='lxml'):
    soup = BeautifulSoup(html, parser)
    if soup is None:
        raise ValueError('Can\'t build DOM tree')

    # Drop comments
    for comment in soup(string=lambda txt: isinstance(txt, Comment)):
        comment.extract()

    # Drop non-meaning tags
    for node in soup(_MEANINGLESS_TAGS):
        node.extract()

    # Drop <pre> wrapper around <code>
    for code in soup('code'):
        if 'pre' != code.parent.name:
            continue
        if 1 != len(code.parent(recursive=False)):
            continue
        code.parent.replace_with(code)

    # Normalize tables
    soup = table_span_normalize(soup)

    html = str(soup)

    extract_kwargs = {
        'filecontent': html,
        'favor_recall': True,
        'output_format': 'html',
    }
    html = trafilatura.extract(**extract_kwargs)

    soup = BeautifulSoup(html, parser)
    if soup is None:
        raise ValueError('Can\'t build DOM tree')

    # Revert <tr> and <td>
    for node in soup('row'):
        node.name = 'tr'
    for node in soup('cell'):
        node.name = 'td'

    html = str(soup)

    html = html.replace('\u0097', '').replace('\u200c', '')

    return html


def fragment_to_markdown(html, parser='lxml'):
    if isinstance(html, str):
        if not len(html.strip()):
            return ''
        soup = BeautifulSoup(html, parser)
        if soup is None:
            raise ValueError('Can\'t build DOM tree')
    elif not isinstance(html, BeautifulSoup):
        raise ValueError(f'Unsupported input type {type(html)}')
    else:
        soup = html

    soup = table_span_normalize(soup)

    converter = MarkdownConverter(strip=['a', 'img'], heading_style='atx')
    md = converter.convert_soup(soup).strip()

    md = re.sub(
        '```.+?```',
        lambda m: m.group(0).strip().replace('\n', '___NEWLINE_HACK___'),
        md, flags=re.S)
    md = re.sub(r'[^\S\n]*\n[^\S\n]*', '\n', md)
    md = re.sub(r'\n{3,}', '\n\n', md)
    md = md.replace('___NEWLINE_HACK___', '\n')
    md = re.sub(r'\n```\n*(.+?)\n*```\n', r'\n```\n\1\n```\n', md, flags=re.S)

    md = md.replace('\n\n— ', '\n* ')
    md = md.replace('\n— ', '\n* ')

    return md


def fragment_to_text(html, parser='lxml'):
    if isinstance(html, str):
        if not len(html.strip()):
            return ''
        soup = BeautifulSoup(html, parser)
        if soup is None:
            raise ValueError('Can\'t build DOM tree')
    elif not isinstance(html, BeautifulSoup):
        raise ValueError(f'Unsupported input type {type(html)}')
    else:
        soup = html

    # Drop comments
    for comment in soup(string=lambda txt: isinstance(txt, Comment)):
        comment.extract()

    # Drop non-meaning tags
    for node in soup(_MEANINGLESS_TAGS):
        node.replace_with(soup.new_tag('br'))

    # Insert linebreaks around block-level tags
    for node in soup(_BLOCKLEVEL_TAGS):
        node.insert_before(soup.new_tag('br'))
        node.insert_before(soup.new_tag('br'))
        node.insert_after(soup.new_tag('br'))
        node.insert_after(soup.new_tag('br'))

    # Remove linebreaks inside text nodes (as browser does)
    for node in soup(string=lambda string: '\n' in string):
        node.string.replace_with(node.string.replace('\n', ' '))

    # Swap html linebreaks to normal ones
    for node in soup('br'):
        node.replace_with('\n')

    # Normalize tables
    soup = table_span_normalize(soup)

    # Cleanup final text
    text = soup.getText()
    text = str(text).strip()
    text = re.sub(' {2,}', ' ', text)
    text = text.replace(' \n', '\n').replace('\n ', '\n')
    text = re.sub('\n{3,}', '\n\n', text)

    return text
