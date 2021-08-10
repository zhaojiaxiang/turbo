from bases import viewsets

from projects.models import Projects
from projects.serializers import ProjectsSerializer
from utils.handlers.handler import get_all_organization_group_belong_me


class ProjectsViewSet(viewsets.APIModelViewSet):
    serializer_class = ProjectsSerializer

    def get_queryset(self):
        all_group_tuple = get_all_organization_group_belong_me(self.request)
        return Projects.objects.filter(organization__in=all_group_tuple)
