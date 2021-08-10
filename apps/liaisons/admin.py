from django.contrib import admin

from liaisons.models import Liaisons


@admin.register(Liaisons)
class LiaisonsAdmin(admin.ModelAdmin):
    list_display = ('fslipno', 'fsystemcd','fprojectcd', 'ftype', 'fodrno')