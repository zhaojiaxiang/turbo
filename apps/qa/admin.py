from django.contrib import admin

from qa.models import QaDetail, QaHead


@admin.register(QaHead)
class QaHeadAdmin(admin.ModelAdmin):
    list_display = ('ftesttyp', 'fsystemcd', 'fprojectcd', 'fslipno', 'fslipno2', 'fobjectid', 'fstatus')


@admin.register(QaDetail)
class QaDetailAdmin(admin.ModelAdmin):
    list_display = ('fcontent', 'fclass1', 'fsortrule', 'fregression', 'fapproval', 'fresult')

