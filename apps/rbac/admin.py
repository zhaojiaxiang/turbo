from django.contrib import admin

from rbac.models import Permission, Role


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ('parent', 'type', 'code', 'content', 'comment', 'is_active')


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name',)
