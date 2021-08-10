import django_filters

from qa.models import QaHead, QaDetail, Qadfproof


class QaHeadFilter(django_filters.rest_framework.FilterSet):
    fslipno = django_filters.CharFilter(field_name='fslipno', lookup_expr='contains')
    fstatus = django_filters.CharFilter(field_name='fstatus', lookup_expr='exact')
    fobjectid = django_filters.CharFilter(field_name='fobjectid', lookup_expr='exact')

    class Meta:
        model = QaHead
        fields = ("fslipno", "fstatus", "fobjectid")


class QaDetailFilter(django_filters.rest_framework.FilterSet):
    qahf = django_filters.CharFilter(field_name='qahf__id', lookup_expr='exact')
    class1 = django_filters.CharFilter(field_name='fclass1', lookup_expr='exact')
    class2 = django_filters.CharFilter(field_name='fclass2', lookup_expr='exact')

    class Meta:
        model = QaDetail
        fields = ("qahf", 'class1', 'class2')


class QaDetailProofFilter(django_filters.rest_framework.FilterSet):
    qadf = django_filters.CharFilter(field_name='qadf_id', lookup_expr='exact')

    class Meta:
        model = Qadfproof
        fields = ("qadf", )
