# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2021/5/30 22:06
# @Author  : https://github.com/536
from django.core.management.base import BaseCommand

from system.tasks import update_wiz


class Command(BaseCommand):
    help = 'Update wiz manually'

    def handle(self, *args, **options):
        update_wiz()
