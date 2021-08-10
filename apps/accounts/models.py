from django.contrib.auth.models import AbstractUser
from django.db import models

from rbac.models import Role, Group, Organizations


class User(AbstractUser):
    """ 用户的基本信息表 """
    name = models.CharField(max_length=30, null=True,
                            unique=True, verbose_name="姓名",
                            error_messages={
                                'unique': '姓名已经在系统中存在'
                            })
    email = models.EmailField(max_length=100, verbose_name="邮箱",
                              unique=True,
                              error_messages={
                                  'unique': '邮箱已经在系统中存在'
                              })
    slmsname = models.CharField(verbose_name="SLIMS系统对应名称", max_length=10, blank=True, null=True)
    redmine_id = models.SmallIntegerField(verbose_name="Red Mine中用户ID", blank=True, null=True)
    frsccd = models.CharField(verbose_name="Man Power中用户ID", max_length=12, blank=True, null=True)
    fmaildays = models.CharField(verbose_name="邮件发送日期（周几）", max_length=150, blank=True, null=True)
    avatar = models.ImageField(verbose_name='用户头像', upload_to='avatar/', null=True, blank=True)
    group = models.ForeignKey(Group, verbose_name="开发组", related_name='group', null=True,
                              blank=True, on_delete=models.DO_NOTHING)

    roles = models.ManyToManyField(Role, verbose_name='拥有的所有角色',
                                   related_name='roles')

    organization = models.ForeignKey(Organizations, verbose_name="组织架构", related_name='organization',
                                     null=True, blank=True, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'users'
        verbose_name = '用户管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
