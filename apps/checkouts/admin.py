from django.contrib import admin

from checkouts.models import CheckOutFiles


@admin.register(CheckOutFiles)
class CheckOutFilesAdmin(admin.ModelAdmin):
    list_display = ('fregisterdte', 'fsystem', 'fcomment', 'fslipno', 'fchkoutobj', 'fchkstatus', 'fchkoutfile')
