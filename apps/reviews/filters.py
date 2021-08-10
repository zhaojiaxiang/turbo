import django_filters

from reviews.models import CodeReview


class ReviewFilter(django_filters.rest_framework.FilterSet):
    """
    CodeReview & DesignReview 的过滤类
    """

    fslipno = django_filters.CharFilter(field_name='fslipno', lookup_expr='contains')
    fobjectid = django_filters.CharFilter(field_name='fobjectid',  lookup_expr='contains')

    class Meta:
        model = CodeReview
        fields = ['fslipno', 'fobjectid']
