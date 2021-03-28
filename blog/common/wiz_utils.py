# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2021/3/28 23:17
# @Author  : https://github.com/536
from datetime import datetime

import mistune
from bs4 import BeautifulSoup
from django.conf import settings
from pygments import highlight
from pygments.formatters import html
from pygments.lexers import get_lexer_by_name
from pygments.util import ClassNotFound
from wiz import Wiz

from article.models import WizCategory, WizDoc


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


def init():
    wiz = Wiz()
    wiz.login(userId=settings.WIZ_USERID, password=settings.WIZ_PASSWORD)

    categories = wiz.get_category().json()['result']
    categories = [name for name in categories if any([
        name.startswith(pattern)
        for pattern in settings.WIZ_CATEGORIES
    ])]

    WizCategory.objects.all().delete()
    WizDoc.objects.all().delete()

    WizCategory.objects.bulk_create(WizCategory(name=name) for name in categories)

    for category in categories:
        docs = wiz.get_notes_of_folder(category=category, withAbstract=False, start=0, count=50).json()['result']
        for doc in docs:
            title = doc['title']
            if not title.endswith('.md'):
                print(title)
                continue

            wiz_doc = WizDoc()
            wiz_doc.guid = doc['docGuid']
            wiz_doc.title = doc['title']
            wiz_doc.version = doc['version']
            wiz_doc.readCount = doc['readCount']
            wiz_doc.created = datetime.utcfromtimestamp(doc['created'] / 1000)
            wiz_doc.accessed = datetime.utcfromtimestamp(doc['accessed'] / 1000)

            doc_text = wiz.get_note_view(docGuid=doc['docGuid']).text
            wiz_doc.text = doc_text

            doc_md = '\n'.join(list(wiz_html_to_md(doc_text)))
            wiz_doc.md = doc_md

            doc_html = markdown(doc_md)
            wiz_doc.html = doc_html

            wiz_doc.Category = WizCategory.objects.get(name=category)
            wiz_doc.save()

    wiz.logout()
