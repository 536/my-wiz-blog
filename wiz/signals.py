# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2021/4/18 1:39
# @Author  : https://github.com/536
from django.db import models
from django.dispatch import receiver
from wiznote import WizNote

from system.models import System
from wiz.models import Share


@receiver(models.signals.post_save, sender=Share)
def post_save(sender, instance, **kwargs):
    if instance.password or instance.expiredAt:
        with WizNote(username=System.objects.get(key='WIZ_USERNAME').value,
                     password=System.objects.get(key='WIZ_PASSWORD').value) as wiz:
            wiz.create_or_update_share(
                docGuid=instance.doc_set.first().guid,
                password=instance.password,
                expiredAt=instance.expiredAt.strftime('%Y-%m-%d %H:%M:%S') if instance.expiredAt else '',
            )
