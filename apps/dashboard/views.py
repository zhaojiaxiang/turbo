from rest_framework.views import APIView

from bases.response import APIResponse
from utils.db.handler import db_connection_execute


class PersonDevelopDetail(APIView):

    def get(self, request):
        user = request.GET.get("name")
        if user is None:
            user = request.user.name

        month_sql = f"""
                    select date_format(fcreatedte, '%Y-%m') create_date 
                        from liaisonf 
                        where fassignedto = '{user}' 
                        group by create_date"""

        month_dict = db_connection_execute(month_sql, 'dict')

        total_sql = f"""
                    select slip_count
                        from (
                                 select date_format(fcreatedte, '%Y-%m') create_date,
                                        count(*)                         slip_count
                                 from liaisonf
                                 where fassignedto = '{user}' 
                                 group by create_date
                                 order by create_date) a"""

        total_dict = db_connection_execute(total_sql, 'dict')

        develop_sql = f"""select ifnull(slip_count, 0) slip_count
                        from (select date_format(fcreatedte, '%Y-%m') create_date, ftype type, count(*) slip_count
                              from liaisonf
                              where fassignedto = '{user}'
                                and ftype = '追加开发'
                              group by create_date, type) a
                                 right outer join
                             (select date_format(fcreatedte, '%Y-%m') create_date
                              from liaisonf
                              where fassignedto = '{user}'
                              group by create_date) b
                             on a.create_date = b.create_date
                        order by b.create_date"""

        develop_dict = db_connection_execute(develop_sql, 'dict')

        req_sql = f"""select ifnull(slip_count, 0) slip_count
                                from (select date_format(fcreatedte, '%Y-%m') create_date, ftype type, count(*) slip_count
                                      from liaisonf
                                      where fassignedto = '{user}'
                                        and ftype = '改善需求'
                                      group by create_date, type) a
                                         right outer join
                                     (select date_format(fcreatedte, '%Y-%m') create_date
                                      from liaisonf
                                      where fassignedto = '{user}'
                                      group by create_date) b
                                     on a.create_date = b.create_date
                                order by b.create_date"""

        req_dict = db_connection_execute(req_sql, 'dict')

        bug_sql = f"""select ifnull(slip_count, 0) slip_count
                        from (select date_format(fcreatedte, '%Y-%m') create_date, ftype type, count(*) slip_count
                              from liaisonf
                              where fassignedto = '{user}'
                                and ftype = '维护阶段障碍'
                              group by create_date, type) a
                                 right outer join
                             (select date_format(fcreatedte, '%Y-%m') create_date
                              from liaisonf
                              where fassignedto = '{user}'
                              group by create_date) b
                             on a.create_date = b.create_date
                        order by b.create_date"""

        bug_dict = db_connection_execute(bug_sql, 'dict')

        month_list = []
        total_list = []
        develop_list = []
        req_list = []
        bug_list = []

        for month in month_dict:
            month_list.append((month['create_date']))

        for total in total_dict:
            total_list.append((total['slip_count']))

        for develop in develop_dict:
            develop_list.append((develop['slip_count']))

        for req in req_dict:
            req_list.append((req['slip_count']))

        for bug in bug_dict:
            bug_list.append((bug['slip_count']))

        data = {}

        data['month'] = month_list
        data['total'] = total_list
        data['develop'] = develop_list
        data['req'] = req_list
        data['bug'] = bug_list

        return APIResponse(data)


class OrganizationDevelopDetail(APIView):

    def get(self, request):
        organization = request.GET.get('organization')

        month_sql = f"""
                            select date_format(fcreatedte, '%Y-%m') create_date 
                                from liaisonf 
                                where forganization = '{organization}' 
                                group by create_date"""

        month_dict = db_connection_execute(month_sql, 'dict')

        total_sql = f"""
                            select slip_count
                                from (
                                         select date_format(fcreatedte, '%Y-%m') create_date,
                                                count(*)                         slip_count
                                         from liaisonf
                                         where forganization = '{organization}' 
                                         group by create_date
                                         order by create_date) a"""

        total_dict = db_connection_execute(total_sql, 'dict')

        develop_sql = f"""select ifnull(slip_count, 0) slip_count
                                from (select date_format(fcreatedte, '%Y-%m') create_date, ftype type, count(*) slip_count
                                      from liaisonf
                                      where forganization = '{organization}' 
                                        and ftype = '追加开发'
                                      group by create_date, type) a
                                         right outer join
                                     (select date_format(fcreatedte, '%Y-%m') create_date
                                      from liaisonf
                                      where forganization = '{organization}' 
                                      group by create_date) b
                                     on a.create_date = b.create_date
                                order by b.create_date"""

        develop_dict = db_connection_execute(develop_sql, 'dict')

        req_sql = f"""select ifnull(slip_count, 0) slip_count
                                        from (select date_format(fcreatedte, '%Y-%m') create_date, ftype type, count(*) slip_count
                                              from liaisonf
                                              where forganization = '{organization}' 
                                                and ftype = '改善需求'
                                              group by create_date, type) a
                                                 right outer join
                                             (select date_format(fcreatedte, '%Y-%m') create_date
                                              from liaisonf
                                              where forganization = '{organization}' 
                                              group by create_date) b
                                             on a.create_date = b.create_date
                                        order by b.create_date"""

        req_dict = db_connection_execute(req_sql, 'dict')

        bug_sql = f"""select ifnull(slip_count, 0) slip_count
                                from (select date_format(fcreatedte, '%Y-%m') create_date, ftype type, count(*) slip_count
                                      from liaisonf
                                      where forganization = '{organization}' 
                                        and ftype = '维护阶段障碍'
                                      group by create_date, type) a
                                         right outer join
                                     (select date_format(fcreatedte, '%Y-%m') create_date
                                      from liaisonf
                                      where forganization = '{organization}' 
                                      group by create_date) b
                                     on a.create_date = b.create_date
                                order by b.create_date"""

        bug_dict = db_connection_execute(bug_sql, 'dict')

        month_list = []
        total_list = []
        develop_list = []
        req_list = []
        bug_list = []

        for month in month_dict:
            month_list.append((month['create_date']))

        for total in total_dict:
            total_list.append((total['slip_count']))

        for develop in develop_dict:
            develop_list.append((develop['slip_count']))

        for req in req_dict:
            req_list.append((req['slip_count']))

        for bug in bug_dict:
            bug_list.append((bug['slip_count']))

        data = {}

        data['month'] = month_list
        data['total'] = total_list
        data['develop'] = develop_list
        data['req'] = req_list
        data['bug'] = bug_list

        return APIResponse(data)


class ProjectTestDetailChart(APIView):

    def get(self, request):
        order_no = request.GET.get('orderno')

        str_sql = f"""
                  select fresult name, count(*) value
                    from qadf
                    where qahf_id in (select id from qahf where fslipno in 
                        (select fslipno from liaisonf where fodrno = '{order_no}'))
                      and fresult in ('OK', 'NGOK')
                    group by fresult
                  """

        project_dict = db_connection_execute(str_sql, 'dict')

        project_name = []
        for project in project_dict:
            project_name.append(project['name'])

        data = {}

        data['name'] = project_name
        data['data'] = project_dict

        return APIResponse(data)
