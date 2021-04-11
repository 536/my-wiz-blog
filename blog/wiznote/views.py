from django.shortcuts import render
from django.views import View

from wiznote.models import Doc, Category, Tag


class CategoryView(View):
    def get(self, request):
        categories = Category.objects.select_related().all()
        return render(request, template_name='wiznote/category.html', context={
            'categories': categories,
        })


class TagView(View):
    def get(self, request):
        tags = Tag.objects.prefetch_related().all()
        return render(request, template_name='wiznote/tag.html', context={
            'tags': tags
        })


class DocView(View):
    def get(self, request, docGuid):
        doc = Doc.objects.select_related().get(guid=docGuid)
        return render(request, template_name='wiznote/doc.html', context={
            'doc': doc
        })
