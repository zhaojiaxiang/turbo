# Generated by Django 2.2.14 on 2021-06-30 21:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='QaDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fclass1', models.CharField(blank=True, db_index=True, max_length=60, null=True, verbose_name='分类1')),
                ('fclass2', models.CharField(blank=True, max_length=60, null=True, verbose_name='分类2')),
                ('fsortrule', models.CharField(blank=True, db_index=True, max_length=100, null=True, verbose_name='排序规则')),
                ('fregression', models.CharField(db_index=True, default='N', max_length=1, verbose_name='回归测试')),
                ('fcontent_text', models.TextField(blank=True, default='', null=True, verbose_name='测试截图')),
                ('fcontent', models.TextField(verbose_name='测试用例')),
                ('ftestdte', models.DateField(blank=True, null=True, verbose_name='测试日期')),
                ('ftestusr', models.CharField(blank=True, max_length=24, null=True, verbose_name='测试者')),
                ('fimpdte', models.DateField(auto_now_add=True, verbose_name='新建日期')),
                ('fimpusr', models.CharField(blank=True, max_length=24, null=True, verbose_name='新建者')),
                ('fapproval', models.CharField(default='N', max_length=1, verbose_name='审核标志')),
                ('fapprovallot', models.IntegerField(default=0, verbose_name='审核批次')),
                ('fresult', models.CharField(blank=True, db_index=True, max_length=10, null=True, verbose_name='测试结果')),
                ('fngcnt', models.SmallIntegerField(default=0, verbose_name='NG次数')),
                ('flastapproveid', models.SmallIntegerField(blank=True, null=True, verbose_name='最后一次审核ID')),
                ('flastsubmitid', models.SmallIntegerField(blank=True, null=True, verbose_name='最后一次提交ID')),
                ('fentdt', models.DateTimeField(auto_now_add=True, verbose_name='登入日期')),
                ('fentusr', models.CharField(blank=True, max_length=24, null=True, verbose_name='登录者')),
                ('fupdtedt', models.DateTimeField(auto_now=True, null=True, verbose_name='更新日期')),
                ('fupdteusr', models.CharField(blank=True, max_length=24, null=True, verbose_name='更新者')),
                ('fupdteprg', models.CharField(blank=True, max_length=110, null=True, verbose_name='更新程序名')),
            ],
            options={
                'verbose_name': '测试明细表',
                'verbose_name_plural': '测试明细表',
                'db_table': 'qadf',
            },
        ),
        migrations.CreateModel(
            name='QaHead',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ftesttyp', models.CharField(db_index=True, max_length=6, verbose_name='测试类型')),
                ('fsystemcd', models.CharField(max_length=20, verbose_name='系统名称')),
                ('fprojectcd', models.CharField(max_length=20, verbose_name='项目名称')),
                ('fslipno', models.CharField(db_index=True, max_length=20, verbose_name='联络票号/订单号')),
                ('fslipno2', models.IntegerField(db_index=True, default=1, verbose_name='订单支号（应用于PCL）')),
                ('fobjectid', models.CharField(db_index=True, max_length=50, verbose_name='测试对象')),
                ('fobjectnm', models.CharField(max_length=50, verbose_name='测试对象')),
                ('fcreatedte', models.DateTimeField(auto_now_add=True, verbose_name='创建日期')),
                ('fcreateusr', models.CharField(max_length=24, verbose_name='创建者')),
                ('fstatus', models.CharField(max_length=1, verbose_name='状态')),
                ('fauditdte', models.DateField(blank=True, null=True, verbose_name='审核日期')),
                ('fauditor', models.CharField(blank=True, max_length=24, null=True, verbose_name='审核者')),
                ('flastapprovallot', models.IntegerField(default=0, verbose_name='最后审核批次')),
                ('ftestdte', models.DateField(blank=True, null=True, verbose_name='测试日期')),
                ('ftestusr', models.CharField(blank=True, max_length=24, null=True, verbose_name='测试者')),
                ('fconfirmdte', models.DateField(blank=True, null=True, verbose_name='确认日期')),
                ('fconfirmusr', models.CharField(blank=True, max_length=24, null=True, verbose_name='确认者')),
                ('fttlcodelines', models.IntegerField(default=0, verbose_name='影响总行数')),
                ('fmodifiedlines', models.SmallIntegerField(default=0, verbose_name='修改行数')),
                ('fcomplexity', models.DecimalField(blank=True, decimal_places=1, max_digits=2, null=True, verbose_name='复杂度')),
                ('fnote', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('fobjmodification', models.TextField(blank=True, null=True, verbose_name='程序修改概要')),
                ('freviewcode', models.TextField(blank=True, null=True, verbose_name='程序确认结果')),
                ('fselflevel', models.CharField(blank=True, max_length=2, null=True, verbose_name='自我评价难易等级')),
                ('flevel', models.CharField(blank=True, max_length=2, null=True, verbose_name='难易等级')),
                ('fentdt', models.DateTimeField(auto_now_add=True, verbose_name='登入日期')),
                ('fentusr', models.CharField(blank=True, max_length=24, null=True, verbose_name='登录者')),
                ('fupdtedt', models.DateTimeField(auto_now=True, null=True, verbose_name='更新日期')),
                ('fupdteusr', models.CharField(blank=True, max_length=24, null=True, verbose_name='更新者')),
                ('fupdteprg', models.CharField(blank=True, max_length=110, null=True, verbose_name='更新程序名')),
            ],
            options={
                'verbose_name': '测试头表',
                'verbose_name_plural': '测试头表',
                'db_table': 'qahf',
            },
        ),
        migrations.CreateModel(
            name='Qadfproof',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fcontent_text', models.TextField(blank=True, default='', null=True, verbose_name='测试截图')),
                ('fentdt', models.DateField(auto_now_add=True, verbose_name='登入日期')),
                ('fentusr', models.CharField(blank=True, max_length=24, null=True, verbose_name='登录者')),
                ('qadf', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='qadf', to='qa.QaDetail')),
            ],
            options={
                'verbose_name': '测试评论表',
                'verbose_name_plural': '测试评论表',
                'db_table': 'qadfproof',
            },
        ),
        migrations.AddField(
            model_name='qadetail',
            name='qahf',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='qahf', to='qa.QaHead'),
        ),
    ]