# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2021/3/28 18:17
# @Author  : https://github.com/536
from django.urls import path

from . import views

app_name = 'article'

urlpatterns = [
    path('', views.Index.as_view()),
    path('<uuid:docGuid>/', views.Article.as_view(), name='article'),
]
