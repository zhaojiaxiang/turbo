from django.contrib import admin

from rbac.models import Permission, Role, Group, Organizations


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ('parent', 'type', 'code', 'content', 'comment', 'is_active')


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', )


@admin.register(Organizations)
class OrganizationsAdmin(admin.ModelAdmin):
    list_display = ('name', 'isgroup')
