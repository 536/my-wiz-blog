# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2021/3/28 23:17
# @Author  : https://github.com/536
from datetime import datetime

import mistune
from bs4 import BeautifulSoup
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from pygments import highlight
from pygments.formatters import html
from pygments.lexers import get_lexer_by_name
from pygments.util import ClassNotFound
from wiz import Wiz

from .models import Category, Doc


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


def create_or_update_categories(wiz):
    categories = wiz.get_category().json()['result']
    for name in categories:
        if name.startswith(settings.WIZ_CATEGORY):
            Category.objects.get_or_create(name=name)
    return Category.objects.all()


def create_or_update_articles(wiz, categories):
    for category in categories:
        wiz_docs = wiz.get_notes_of_folder(category=category.name, withAbstract=False, start=0, count=50).json()[
            'result']
        for wiz_doc in wiz_docs:
            if not wiz_doc['title'].endswith('.md'):
                continue

            doc_text = wiz.get_note_view(docGuid=wiz_doc['docGuid']).text
            doc_md = '\n'.join(list(wiz_html_to_md(doc_text)))
            doc_html = markdown(doc_md)

            try:
                doc = Doc.objects.get(guid=wiz_doc['docGuid'])
            except ObjectDoesNotExist:
                Doc.objects.create(
                    guid=wiz_doc['docGuid'],
                    title=wiz_doc['title'],
                    version=wiz_doc['version'],
                    readCount=wiz_doc['readCount'],
                    created=datetime.utcfromtimestamp(wiz_doc['created'] / 1000),
                    accessed=datetime.utcfromtimestamp(wiz_doc['accessed'] / 1000),
                    text=doc_text,
                    md=doc_md,
                    html=doc_html,
                    Category=category
                )
            else:
                if doc.version != wiz_doc['version']:
                    doc.update(
                        title=wiz_doc['title'],
                        version=wiz_doc['version'],
                        readCount=wiz_doc['readCount'],
                        accessed=datetime.utcfromtimestamp(wiz_doc['accessed'] / 1000),
                        text=doc_text,
                        md=doc_md,
                        html=doc_html,
                        Category=category
                    )


def wiz_init():
    wiz = Wiz()
    wiz.login(userId=settings.WIZ_USERID, password=settings.WIZ_PASSWORD)

    categories = create_or_update_categories(wiz)
    create_or_update_articles(wiz, categories)

    wiz.logout()
