from django.core.cache import cache
from django.shortcuts import render
from django.views import View

from article.models import WizCategory, WizDoc
from common.wiz_utils import init


class Index(View):
    def get(self, request):
        if not cache.get('inited'):
            init()
            cache.set('inited', True, 60 * 60)
        categories = WizCategory.objects.all()
        docs = WizDoc.objects.all()
        return render(request, template_name='index.html', context={
            'categories': categories,
            'docs': docs
        })


class Article(View):
    def get(self, request, docGuid):
        doc = WizDoc.objects.get(guid=docGuid)
        return render(request, template_name='article.html', context={
            'doc': doc
        })
