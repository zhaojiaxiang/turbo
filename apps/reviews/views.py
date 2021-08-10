from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters

from bases import mixins
from reviews.filters import ReviewFilter
from reviews.models import CodeReview
from reviews.serializers import DesignReviewSerializer, CodeReviewSerializer


class DesignReviewViewSet(mixins.APIListModelMixin, mixins.APIRetrieveModelMixin, mixins.APICreateModelMixin,
                          mixins.APIUpdateModelMixin, viewsets.GenericViewSet):

    def get_queryset(self):
        return CodeReview.objects.filter(fobjectid__exact="Design Review")

    serializer_class = DesignReviewSerializer

    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filter_class = ReviewFilter


class CodeReviewViewSet(mixins.APIListModelMixin, mixins.APIRetrieveModelMixin, mixins.APICreateModelMixin,
                        mixins.APIUpdateModelMixin, viewsets.GenericViewSet):
    def get_queryset(self):
        # Django 中不等于的处理方式，使用~Q，Q是处理等于
        return CodeReview.objects.filter(~Q(fobjectid="Design Review"))

    serializer_class = CodeReviewSerializer

    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filter_class = ReviewFilter
