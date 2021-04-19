# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2021/4/11 16:36
# @Author  : https://github.com/536
from django.core.cache import cache

from .models import System


def system(request):
    title_prefix = cache.get_or_set('title_prefix', System.objects.get_key('TITLE_PREFIX', 'Hi'), 10 * 60)
    social_github = cache.get_or_set('social_github',
                                     System.objects.get_key('SOCIAL_GITHUB'), 10 * 60)
    return {
        'SYSTEM_TITLE_PREFIX': title_prefix,
        'SYSTEM_SOCIAL_GITHUB': social_github,
    }
