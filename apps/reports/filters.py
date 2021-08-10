import django_filters

from liaisons.models import Liaisons
from qa.models import QaHead


class ReportLiaisonsFilter(django_filters.rest_framework.FilterSet):
    """
    Report Liaison的过滤类
    """
    fsystemcd = django_filters.CharFilter(field_name='fsystemcd',  lookup_expr='exact')
    fprojectcd = django_filters.CharFilter(field_name='fprojectcd', lookup_expr='exact')
    fodrno = django_filters.CharFilter(field_name='fodrno', lookup_expr='contains')

    class Meta:
        model = Liaisons
        fields = ['fsystemcd', 'fprojectcd', 'fodrno']


class QaHeadFilter(django_filters.rest_framework.FilterSet):
    """
    Report Liaison的过滤类
    """

    fodrno = django_filters.CharFilter(field_name='fslipno', lookup_expr='contains')

    class Meta:
        model = QaHead
        fields = ['fodrno']
