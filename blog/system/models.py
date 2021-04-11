from django.db import models


class SystemManager(models.Manager):
    def get_key(self, key: str, default: any = None):
        try:
            value = self.get(key=key).value
        except self.DoesNotExist:
            value = default
        return value


class System(models.Model):
    objects = SystemManager()

    key = models.CharField(max_length=100, primary_key=True, verbose_name='系统设置KEY')
    value = models.CharField(max_length=200, verbose_name='系统设置VALUE')
