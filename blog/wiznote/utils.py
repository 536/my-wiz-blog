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
            formatter = html.HtmlFormatter()
            return highlight(code, lexer, formatter)
        return '<pre><code>' + mistune.escape(code) + '</code></pre>'


def wiz_html_to_md(content: str):
    soup = BeautifulSoup(content, features='html.parser')
    for div in soup.find_all('div'):
        yield div.get_text().replace('\xa0', ' ')


markdown = mistune.create_markdown(renderer=HighlightRenderer(), escape=True)
