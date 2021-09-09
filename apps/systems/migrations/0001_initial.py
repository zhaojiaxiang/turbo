# Generated by Django 2.2.14 on 2021-06-30 21:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('rbac', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Systems',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fsystemcd', models.CharField(max_length=20, verbose_name='系统代码')),
                ('fsystemnm', models.CharField(max_length=50, verbose_name='系统名称')),
                ('fentdt', models.DateField(blank=True, null=True, verbose_name='登入日期')),
                ('fentusr', models.CharField(blank=True, max_length=24, null=True, verbose_name='登录者')),
                ('fupdtedt', models.DateField(blank=True, null=True, verbose_name='更新日期')),
                ('fupdteusr', models.CharField(blank=True, max_length=24, null=True, verbose_name='更新者')),
                ('fupdteprg', models.CharField(blank=True, max_length=110, null=True, verbose_name='更新程序名')),
                ('organization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='system_organization', to='rbac.Organizations', verbose_name='组织构架中组名')),
            ],
            options={
                'verbose_name': '系统代码',
                'verbose_name_plural': '系统代码',
                'db_table': 'systemm',
            },
        ),
    ]