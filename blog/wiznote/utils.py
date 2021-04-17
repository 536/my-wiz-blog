# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2021/3/28 23:17
# @Author  : https://github.com/536
import mistune
from bs4 import BeautifulSoup
from pygments import highlight
from pygments.formatters import html
from pygments.lexers import get_lexer_by_name
from pygments.util import ClassNotFound


class HighlightRenderer(mistune.HTMLRenderer):
    def block_code(self, code, lang=None):
        if lang:
            try:
                lexer = get_lexer_by_name(lang, stripall=True)
            except ClassNotFound:
                lexer = get_lexer_by_name('text', stripall=True)
            formatter = html.HtmlFormatter(linenos='inline')
            text = highlight(code, lexer, formatter)
            text = text[:27] + ' lang="' + lang + '"' + text[27:]
        else:
            text = '<pre lang="%s"><code>%s</code></pre>' % (lang, mistune.escape(code))
        return text


def wiz_html_to_md(content: str):
    def recursive_div(div_element):
        div_as_md = []
        for element in div_element.contents:
            if element.name == 'div':
                div_as_md.append('\n')
                div_as_md.extend(recursive_div(element))
            else:
                div_as_md.append(str(element)
                                 .replace('\xa0', ' ')
                                 .replace('<br/>', '\n'))
        return ''.join(div_as_md)

    soup = BeautifulSoup(content, features='html.parser')
    for div in soup.body.find_all('div', recursive=False):
        yield recursive_div(div)


markdown = mistune.create_markdown(renderer=HighlightRenderer(), escape=True)
