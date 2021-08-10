import django_filters

from liaisons.models import Liaisons


class LiaisonsFilter(django_filters.rest_framework.FilterSet):
    """
    Liaison的过滤类
    """
    fsystemcd = django_filters.CharFilter(field_name='fsystemcd',  lookup_expr='exact')
    fprojectcd = django_filters.CharFilter(field_name='fprojectcd', lookup_expr='exact')
    fslipno = django_filters.CharFilter(field_name='fslipno', lookup_expr='contains')
    ftype = django_filters.CharFilter(field_name='ftype',  lookup_expr='contains')
    fstatus = django_filters.CharFilter(field_name='fstatus', lookup_expr='exact')
    fodrno = django_filters.CharFilter(field_name='fodrno', lookup_expr='contains')
    fleader = django_filters.CharFilter(field_name='fleader', lookup_expr='contains')
    fhelper = django_filters.CharFilter(field_name='fhelper',  lookup_expr='contains')
    fassignedto = django_filters.CharFilter(field_name='fassignedto',  lookup_expr='contains')
    fsirno = django_filters.CharFilter(field_name='fsirno',  lookup_expr='contains')

    class Meta:
        model = Liaisons
        fields = ['fsystemcd', 'fprojectcd', 'fslipno', 'ftype', 'fstatus', 'fodrno', 'fleader', 'fhelper',
                  'fassignedto', 'fsirno']


class QAProjectFilter(django_filters.rest_framework.FilterSet):
    """
    QA Project的过滤类
    """
    fprojectcd = django_filters.CharFilter(field_name='fprojectcd', lookup_expr='exact')
    fodrno = django_filters.CharFilter(field_name='fodrno', lookup_expr='contains')
    forganization = django_filters.NumberFilter(field_name='forganization', lookup_expr='contains')

    class Meta:
        model = Liaisons
        fields = ['fprojectcd', 'fodrno', 'forganization']


class QAProjectDataStatisticsFilter(django_filters.rest_framework.FilterSet):
    """
    订单下联络票的测试数据统计的过滤类
    """
    fodrno = django_filters.CharFilter(field_name='fodrno', lookup_expr='exact')

    class Meta:
        model = Liaisons
        fields = ['fodrno']
