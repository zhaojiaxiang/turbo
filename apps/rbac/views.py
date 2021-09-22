from rest_framework import views
from rest_framework.viewsets import GenericViewSet

from bases import mixins
from bases.response import APIResponse
from rbac.models import Organizations
from rbac.serializers import OrganizationsSerializer
from utils.db.handler import db_connection_execute
from utils.handlers.handler import get_all_organization_group_belong_me, get_all_organizations


class WorkingOrganization(views.APIView):

    def get(self, request):
        organization_group_tuple = get_all_organization_group_belong_me(request)
        str_sql = f"select distinct a.id, a.name from organizations a, projectm b where " \
            f"a.id = b.organization_id and a.id in {organization_group_tuple} order by a.name desc"

        working_organization = db_connection_execute(str_sql, 'dict')

        return APIResponse(data=working_organization)


class PersonInOrganization(views.APIView):

    def get(self, request):
        organization = request.GET.get('organization')
        all_organizations = get_all_organizations(organization)
        str_sql = f"select name from users where users.organization_id in {all_organizations} and is_active='1' "

        persons = db_connection_execute(str_sql, 'dict')

        return APIResponse(data=persons)


class WorkingProject(views.APIView):

    def get(self, request):

        organization = request.GET.get('organization')
        organization_group_tuple = get_all_organization_group_belong_me(request)
        if organization:
            organization_group_tuple = (organization, organization)

        str_sql = f"select b.fprojectcd id, a.name, b.id keyid from organizations a, projectm b where " \
            f"a.id = b.organization_id and a.id in {organization_group_tuple} order by a.name desc, b.fprojectcd desc"

        working_project = db_connection_execute(str_sql, 'dict')

        return APIResponse(data=working_project)


class OrganizationsViewSet(mixins.APIRetrieveModelMixin, mixins.APIListModelMixin, GenericViewSet):

    serializer_class = OrganizationsSerializer
    queryset = Organizations.objects.all()
