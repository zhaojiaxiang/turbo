from bases import viewsets
from systems.models import Systems
from systems.serializers import SystemsSerializer
from utils.handlers.handler import get_all_organization_group_belong_me


class SystemsViewSet(viewsets.APIModelViewSet):
    serializer_class = SystemsSerializer

    def get_queryset(self):
        all_group_tuple = get_all_organization_group_belong_me(self.request)
        return Systems.objects.filter(organization__in=all_group_tuple)
