# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2021/3/28 18:17
# @Author  : https://github.com/536
from django.urls import path

from . import views

app_name = 'wiznote'

urlpatterns = [
    path('category/', views.CategoryView.as_view(), name='category'),
    path('tags/', views.TagsView.as_view(), name='tags'),
    path('tag/<uuid:guid>/', views.TagView.as_view(), name='tag'),
    path('doc/<uuid:guid>/', views.DocView.as_view(), name='doc'),
]
