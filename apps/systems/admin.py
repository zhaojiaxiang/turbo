from django.contrib import admin

from systems.models import Systems


@admin.register(Systems)
class SystemsAdmin(admin.ModelAdmin):
    list_display = ('fsystemcd', 'fsystemnm', 'organization')
