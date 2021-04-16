from django.shortcuts import render
from django.views import View

from wiznote.models import Doc, Category, Tag


class CategoryView(View):
    def get(self, request):
        docs = Doc.objects.select_related().all()
        return render(request, template_name='wiznote/category.html', context={
            'docs': docs,
        })


class TagsView(View):
    def get(self, request):
        tags = Tag.objects.prefetch_related().all()
        return render(request, template_name='wiznote/tags.html', context={
            'tags': tags
        })


class TagView(View):
    def get(self, request, guid):
        tag = Tag.objects.prefetch_related().get(guid=guid)
        return render(request, template_name='wiznote/tag.html', context={
            'tag': tag
        })


class DocView(View):
    def get(self, request, guid):
        doc = Doc.objects.select_related().get(guid=guid)
        return render(request, template_name='wiznote/doc.html', context={
            'doc': doc
        })
