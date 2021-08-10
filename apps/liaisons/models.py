from django.db import models


class Liaisons(models.Model):
    fsystemcd = models.CharField(verbose_name='系统名称', max_length=20)
    fprojectcd = models.CharField(verbose_name='项目名称', max_length=20)
    fslipno = models.CharField(db_index=True, verbose_name='联络票号', max_length=20)
    ftype = models.CharField(verbose_name='类型', max_length=10)
    fstatus = models.CharField(verbose_name='状态', max_length=15)
    fodrno = models.CharField(db_index=True, verbose_name='订单号', max_length=20)
    fcreatedte = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    fcreateusr = models.CharField(verbose_name='创建者', max_length=24)
    fassignedto = models.CharField(db_index=True, verbose_name='对应者', max_length=60)
    fhelper = models.CharField(db_index=True, verbose_name='协助者', max_length=60, null=True, blank=True)
    fleader = models.CharField(db_index=True, verbose_name='负责人', max_length=60, null=True, blank=True)
    fbrief = models.TextField(verbose_name='开发描述')
    fcontent = models.TextField(verbose_name='问题描述', null=True, blank=True)
    fanalyse = models.TextField(verbose_name='问题分析', null=True, blank=True)
    fsolution = models.TextField(verbose_name='解决方案', null=True, blank=True)
    fplnstart = models.DateField(verbose_name='计划开始日期')
    fplnend = models.DateField(verbose_name='计划结束日期')
    factstart = models.DateField(verbose_name='实际开始日期', null=True, blank=True)
    factend = models.DateField(verbose_name='实际结束日期', null=True, blank=True)
    freleasedt = models.DateField(verbose_name='程序发布日期', null=True, blank=True)
    fplnmanpower = models.DecimalField(verbose_name='预计工数', max_digits=5, decimal_places=1, null=True, blank=True)
    factmanpower = models.DecimalField(verbose_name='实际工数', max_digits=5, decimal_places=1, null=True, blank=True)
    freleaserpt = models.CharField(verbose_name='程序发布报告URL', max_length=200, null=True, blank=True)
    fsirno = models.CharField(verbose_name='SIR号', max_length=10, null=True, blank=True)
    forganization = models.IntegerField(verbose_name='组织构架中组名', null=True, blank=True)  # 不再使用外键
    fentdt = models.DateTimeField(verbose_name='登入日期', auto_now_add=True)
    fentusr = models.CharField(verbose_name='登录者', max_length=24, null=True, blank=True)
    fupdtedt = models.DateTimeField(verbose_name='更新日期', null=True, blank=True, auto_now=True)
    fupdteusr = models.CharField(verbose_name='更新者', max_length=24, null=True, blank=True)
    fupdteprg = models.CharField(verbose_name='更新程序名', max_length=110, null=True, blank=True)

    class Meta:
        db_table = 'liaisonf'
        verbose_name = '联络票'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.fslipno

