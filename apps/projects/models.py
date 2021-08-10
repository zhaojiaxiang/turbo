from django.db import models

from rbac.models import Organizations


class Projects(models.Model):
    fprojectcd = models.CharField(verbose_name='项目代码', max_length=20)
    fprojectnm = models.CharField(verbose_name='项目名称', null=True, blank=True, max_length=50)
    fprojectsn = models.CharField(verbose_name='项目', null=True, blank=True, max_length=10)
    fautoflg = models.CharField(verbose_name='自动生成联络票号', null=True, blank=True, max_length=1)
    fentdt = models.DateField(verbose_name='登入日期', auto_now_add=True)
    fentusr = models.CharField(verbose_name='登录者', max_length=24, null=True, blank=True)
    fupdtedt = models.DateField(verbose_name='更新日期', null=True, blank=True)
    fupdteusr = models.CharField(verbose_name='更新者', max_length=24, null=True, blank=True)
    fupdteprg = models.CharField(verbose_name='更新程序名', max_length=110, null=True, blank=True)
    organization = models.ForeignKey(Organizations, verbose_name='组织构架中组名', related_name='project_organization',
                                     blank=True, null=True, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'projectm'
        verbose_name = '项目代码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.fprojectcd
