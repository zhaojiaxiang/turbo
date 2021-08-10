from django.db import models

from rbac.models import Organizations


class Systems(models.Model):
    fsystemcd = models.CharField(verbose_name='系统代码', max_length=20)
    fsystemnm = models.CharField(verbose_name='系统名称', max_length=50)
    fentdt = models.DateField(verbose_name='登入日期', null=True, blank=True)
    fentusr = models.CharField(verbose_name='登录者', max_length=24, null=True, blank=True)
    fupdtedt = models.DateField(verbose_name='更新日期', null=True, blank=True)
    fupdteusr = models.CharField(verbose_name='更新者', max_length=24, null=True, blank=True)
    fupdteprg = models.CharField(verbose_name='更新程序名', max_length=110, null=True, blank=True)
    organization = models.ForeignKey(Organizations, verbose_name='组织构架中组名', related_name='system_organization',
                                     blank=True, null=True, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'systemm'
        verbose_name = '系统代码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.fsystemcd
