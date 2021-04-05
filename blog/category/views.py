from django.shortcuts import render
from django.views import View

from main.models import Category, Doc


class CategoryView(View):
    def get(self, request):
        categories = Category.objects.all()
        docs = Doc.objects.all()
        return render(request, template_name='category/index.html', context={
            'categories': categories,
            'docs': docs
        })


class ArticleView(View):
    def get(self, request, docGuid):
        doc = Doc.objects.get(guid=docGuid)
        return render(request, template_name='category/article.html', context={
            'doc': doc
        })
