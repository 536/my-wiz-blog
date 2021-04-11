from django.shortcuts import render
from django.views import View

from wiznote.models import Doc, Category


class CategoryView(View):
    def get(self, request):
        categories = Category.objects.select_related().all()
        return render(request, template_name='wiznote/category.html', context={
            'categories': categories,
        })


class TagsView(View):
    def get(self, request):
        return render(request, 'wiznote/tags.html')


class DocView(View):
    def get(self, request, docGuid):
        doc = Doc.objects.select_related().get(guid=docGuid)
        return render(request, template_name='wiznote/doc.html', context={
            'doc': doc
        })
