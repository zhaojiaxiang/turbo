import django_filters

from checkouts.models import CheckOutFiles


class CheckOutFilesFilter(django_filters.rest_framework.FilterSet):
    """
    CheckOutFiles的过滤类
    """
    fsystem = django_filters.CharFilter(field_name='fsystem',  lookup_expr='exact')
    fslipno = django_filters.CharFilter(field_name='fslipno', lookup_expr='contains')
    fchkoutobj = django_filters.CharFilter(field_name='fchkoutobj',  lookup_expr='contains')
    fchkstatus = django_filters.CharFilter(field_name='fchkstatus', lookup_expr='exact')
    fapplicant = django_filters.CharFilter(field_name='fapplicant', lookup_expr='contains')
    fchkoutfile = django_filters.CharFilter(field_name='fchkoutfile', lookup_expr='contains')

    class Meta:
        model = CheckOutFiles
        fields = ['fsystem', 'fslipno', 'fchkoutobj', 'fchkstatus', 'fapplicant', 'fchkoutfile']
