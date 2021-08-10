from django.db import models


class Permission(models.Model):
    """
    权限控制主表
    """
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.DO_NOTHING)
    type = models.CharField(max_length=20, verbose_name="类型")
    code = models.CharField(max_length=20, verbose_name="权限代码")
    content = models.CharField(max_length=200, verbose_name="权限内容", unique=True)
    comment = models.CharField(max_length=200, verbose_name="权限内容说明")
    is_active = models.BooleanField(verbose_name="是否有效", default=True)

    class Meta:
        db_table = 'permission'
        verbose_name = '权限主表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.content


class Role(models.Model):
    """
    角色
    """
    name = models.CharField(verbose_name='角色名称', max_length=32)
    permission = models.ManyToManyField(verbose_name='拥有的所有权限', to='Permission', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "roles"
        verbose_name = "角色"
        verbose_name_plural = verbose_name


class Group(models.Model):
    """
    该组别与权限无关
    """
    name = models.CharField(verbose_name='组名', max_length=32)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "groups"
        verbose_name = "开发组"
        verbose_name_plural = verbose_name


class Organizations(models.Model):
    """
    组织架构
    """
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.DO_NOTHING)
    name = models.CharField('组织架构名称', max_length=64)
    isgroup = models.BooleanField('是否是组', default=True)
    permission = models.ManyToManyField(verbose_name='拥有的所有权限', to='Permission', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "organizations"
        verbose_name = "组织架构"
        verbose_name_plural = verbose_name
