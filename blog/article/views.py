from django.shortcuts import render
from django.views import View

from main.models import Category, Doc


class Index(View):
    def get(self, request):
        categories = Category.objects.all()
        docs = Doc.objects.all()
        return render(request, template_name='article/index.html', context={
            'categories': categories,
            'docs': docs
        })


class Article(View):
    def get(self, request, docGuid):
        doc = Doc.objects.get(guid=docGuid)
        return render(request, template_name='article/article.html', context={
            'doc': doc
        })
