from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_page


@method_decorator(cache_page(60 * 60 * 24), name='dispatch')
class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')


@method_decorator(cache_page(60 * 60 * 24), name='dispatch')
class AboutView(View):
    def get(self, request):
        return render(request, 'about.html')
