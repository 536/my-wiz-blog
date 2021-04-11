# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2021/4/11 16:36
# @Author  : https://github.com/536
from django.conf import settings


def system(request):
    return {
        'SYSTEM_TITLE_PREFIX': settings.SYSTEM_TITLE_PREFIX,
        'SYSTEM_SOCIAL_GITHUB': settings.SYSTEM_SOCIAL_GITHUB,
    }
