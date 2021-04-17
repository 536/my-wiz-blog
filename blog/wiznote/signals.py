# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2021/4/18 1:39
# @Author  : https://github.com/536
from django.db import models
from django.dispatch import receiver

from wiznote.models import Resource


@receiver(models.signals.pre_delete, sender=Resource)
def auto_delete_file_on_change(sender, instance, **kwargs):
    instance.file.delete()
