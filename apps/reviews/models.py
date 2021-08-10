from django.db import models


class CodeReview(models.Model):
    """
    代码Review 和 设计Review维护在一张表中
    当是设计Review时， fobjectid为："Design Review"
    """
    fslipno = models.CharField(verbose_name='联络票号', max_length=20)
    fobjectid = models.CharField(verbose_name='Review对象', max_length=100)
    fcontent_text = models.TextField(verbose_name='Review内容', default='')
    fentdt = models.DateField(verbose_name='登入日期', auto_now_add=True)
    fentusr = models.CharField(verbose_name='登录者', max_length=24, null=True, blank=True)
    fupdtedt = models.DateField(verbose_name='更新日期', null=True, blank=True)
    fupdteusr = models.CharField(verbose_name='更新者', max_length=24, null=True, blank=True)
    fupdteprg = models.CharField(verbose_name='更新程序名', max_length=110, null=True, blank=True)

    class Meta:
        db_table = 'codereview'
        verbose_name = '设计or代码Review'
        verbose_name_plural = verbose_name
