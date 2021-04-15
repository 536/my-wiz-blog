# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2021/4/11 16:36
# @Author  : https://github.com/536
from .models import System


def system(request):
    return {
        'SYSTEM_TITLE_PREFIX': System.objects.get_key('TITLE_PREFIX', 'Hi'),
        'SYSTEM_SOCIAL_GITHUB': System.objects.get_key('SOCIAL_GITHUB', 'https://github.com/536/'),
    }
