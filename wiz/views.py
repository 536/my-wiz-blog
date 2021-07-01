from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import View

from wiz.models import Doc, Tag


class CategoryView(View):
    def get(self, request, page: int = 1):
        docs = Doc.objects.all()
        paginator = Paginator(docs.order_by('-created'), 10)
        return render(request, template_name='wiznote/category.html', context={
            'page': paginator.get_page(page),
            'pageRange': paginator.get_elided_page_range(page, on_ends=0),
            'ellipsis': paginator.ELLIPSIS,
        })


class TagsView(View):
    def get(self, request):
        tags = Tag.objects.all()
        return render(request, template_name='wiznote/tags.html', context={
            'tags': tags
        })


class TagView(View):
    def get(self, request, guid):
        tag = Tag.objects.prefetch_related().get(guid=guid)
        return render(request, template_name='wiznote/tag.html', context={
            'tag': tag
        })
