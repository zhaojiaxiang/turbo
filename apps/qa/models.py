from django.db import models


class QaHead(models.Model):
    ftesttyp = models.CharField(db_index=True, verbose_name='测试类型', max_length=6)
    fsystemcd = models.CharField(verbose_name='系统名称', max_length=20)
    fprojectcd = models.CharField(verbose_name='项目名称', max_length=20)
    fslipno = models.CharField(db_index=True, verbose_name='联络票号/订单号', max_length=20)
    fslipno2 = models.IntegerField(db_index=True, verbose_name='订单支号（应用于PCL）', default=1)
    fobjectid = models.CharField(db_index=True, verbose_name='测试对象', max_length=50)
    fobjectnm = models.CharField(verbose_name='测试对象', max_length=50)
    fcreatedte = models.DateTimeField(verbose_name='创建日期', auto_now_add=True)
    fcreateusr = models.CharField(verbose_name='创建者', max_length=24)
    fstatus = models.CharField(verbose_name='状态', max_length=1)
    fauditdte = models.DateField(verbose_name='审核日期', null=True, blank=True)
    fauditor = models.CharField(verbose_name='审核者', max_length=24, null=True, blank=True)
    flastapprovallot = models.IntegerField(verbose_name='最后审核批次', default=0)
    ftestdte = models.DateField(verbose_name='测试日期', null=True, blank=True)
    ftestusr = models.CharField(verbose_name='测试者', max_length=24, null=True, blank=True)
    fconfirmdte = models.DateField(verbose_name='确认日期', null=True, blank=True)
    fconfirmusr = models.CharField(verbose_name='确认者', max_length=24, null=True, blank=True)
    fttlcodelines = models.IntegerField(verbose_name='影响总行数', default=0)
    fmodifiedlines = models.SmallIntegerField(verbose_name='修改行数', default=0)
    fcomplexity = models.DecimalField(verbose_name='复杂度', max_digits=2, decimal_places=1, null=True, blank=True)
    # 2021-10-11 赵加响 原始目标测试数量计算方式只针对PB开发，现在允许手动输入目标测试数以及目标NG数
    ftargettest = models.IntegerField(verbose_name='目标测试数(不包含回归)', default=0)
    ftargetregtest = models.IntegerField(verbose_name='目标回归测试数', default=0)
    ftargetng = models.IntegerField(verbose_name='目标回归NG数', default=0)
    # 2021-10-11 赵加响
    fnote = models.TextField(verbose_name='备注', null=True, blank=True)
    fobjmodification = models.TextField(verbose_name='程序修改概要', null=True, blank=True)
    freviewcode = models.TextField(verbose_name='程序确认结果', null=True, blank=True)
    fselflevel = models.CharField(verbose_name='自我评价难易等级', max_length=2, null=True, blank=True)
    flevel = models.CharField(verbose_name='难易等级', max_length=2, null=True, blank=True)
    fentdt = models.DateTimeField(verbose_name='登入日期', auto_now_add=True)
    fentusr = models.CharField(verbose_name='登录者', max_length=24, null=True, blank=True)
    fupdtedt = models.DateTimeField(verbose_name='更新日期', null=True, blank=True, auto_now=True)
    fupdteusr = models.CharField(verbose_name='更新者', max_length=24, null=True, blank=True)
    fupdteprg = models.CharField(verbose_name='更新程序名', max_length=110, null=True, blank=True)

    class Meta:
        db_table = 'qahf'
        verbose_name = '测试头表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.fobjectid


class QaDetail(models.Model):
    fclass1 = models.CharField(db_index=True, verbose_name='分类1', max_length=60, null=True, blank=True)
    fclass2 = models.CharField(verbose_name='分类2', max_length=60, null=True, blank=True)
    fsortrule = models.CharField(db_index=True, verbose_name='排序规则', max_length=100, null=True, blank=True)
    fregression = models.CharField(db_index=True, verbose_name='回归测试', max_length=1, default='N')
    fcontent_text = models.TextField(verbose_name='测试截图', default='', null=True, blank=True)
    fcontent = models.TextField(verbose_name='测试用例')
    ftestdte = models.DateField(verbose_name='测试日期', null=True, blank=True)
    ftestusr = models.CharField(verbose_name='测试者', max_length=24, null=True, blank=True)
    fimpdte = models.DateField(verbose_name='新建日期', auto_now_add=True)
    fimpusr = models.CharField(verbose_name='新建者', max_length=24, null=True, blank=True)
    fapproval = models.CharField(verbose_name='审核标志', max_length=1, default='N')
    fapprovallot = models.IntegerField(verbose_name='审核批次', default=0)
    fresult = models.CharField(db_index=True, verbose_name='测试结果', max_length=10, null=True, blank=True)
    fngcnt = models.SmallIntegerField(verbose_name='NG次数', default=0)
    flastapproveid = models.SmallIntegerField(verbose_name="最后一次审核ID", null=True, blank=True)
    flastsubmitid = models.SmallIntegerField(verbose_name="最后一次提交ID", null=True, blank=True)
    qahf = models.ForeignKey(QaHead, related_name='qahf', on_delete=models.CASCADE)
    fentdt = models.DateTimeField(verbose_name='登入日期', auto_now_add=True)
    fentusr = models.CharField(verbose_name='登录者', max_length=24, null=True, blank=True)
    fupdtedt = models.DateTimeField(verbose_name='更新日期', null=True, blank=True, auto_now=True)
    fupdteusr = models.CharField(verbose_name='更新者', max_length=24, null=True, blank=True)
    fupdteprg = models.CharField(verbose_name='更新程序名', max_length=110, null=True, blank=True)

    class Meta:
        db_table = 'qadf'
        verbose_name = '测试明细表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.fcontent


class Qadfproof(models.Model):
    """
    将保存测试截图字段分离出来，同时管理对测试结果的评论
    有评论的测试结果将自动默认为 NG，且评论次数就是NG次数
    """
    fcontent_text = models.TextField(verbose_name='测试截图', default='', null=True, blank=True)
    fentdt = models.DateField(verbose_name='登入日期', auto_now_add=True)
    fentusr = models.CharField(verbose_name='登录者', max_length=24, null=True, blank=True)
    qadf = models.ForeignKey(QaDetail, related_name='qadf', on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'qadfproof'
        verbose_name = '测试评论表'
        verbose_name_plural = verbose_name
