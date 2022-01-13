from rest_framework.views import APIView

from bases.response import APIResponse
from utils.db.handler import db_connection_execute, query_single_with_no_parameter
from utils.handlers.handler import get_all_organization_group_belong_me


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

        # todo 此处统计忽略了 type = '维护阶段障碍'
        total_sql = f"""
                    select slip_count
                        from (
                                 select date_format(fcreatedte, '%Y-%m') create_date,
                                        count(*)                         slip_count
                                 from liaisonf
                                 where fassignedto = '{user}' and ftype <> '维护阶段障碍'
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
                                         where forganization = '{organization}' and ftype <> '维护阶段障碍'
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


class LiaisonTypeScaleChart(APIView):

    def get(self, request):
        organizations = get_all_organization_group_belong_me(request)

        str_sql = f"""
                    select ftype name, count(*) value
                        from liaisonf
                        where forganization in {organizations}
                          and fcreatedte between date_sub(now(), interval 6 month) and now()
                        group by ftype
                    """

        type_dict = db_connection_execute(str_sql, 'dict')
        return APIResponse(type_dict)


class LiaisonPlanActualManPowerChart(APIView):

    def get(self, request):
        organizations = get_all_organization_group_belong_me(request)

        str_sql = f"""
                   select date_format(fcreatedte, '%Y-%m') month, sum(fplnmanpower) plan, sum(factmanpower) actual
                        from liaisonf
                        where forganization in {organizations}
                          and fcreatedte between date_sub(now(), interval 6 month) and now()
                        group by month
                   """

        power_dict = db_connection_execute(str_sql, 'dict')

        month = []
        plan = []
        actual = []
        for power in power_dict:
            month.append(power['month'])
            plan.append(power['plan'])
            actual.append(power['actual'])

        data = {}

        data['month'] = month
        data['plan'] = plan
        data['actual'] = actual

        return APIResponse(data)


class LiaisonTypeManPowerScaleChart(APIView):

    def get(self, request):
        organizations = get_all_organization_group_belong_me(request)
        project_sql = f"""
                      select projectm.fprojectsn project
                            from liaisonf, projectm
                            where forganization in {organizations}
                              and liaisonf.fprojectcd = projectm.fprojectcd
                              and fcreatedte between date_sub(now(), interval 6 month) and now()
                            group by project
                      """

        project_dict = db_connection_execute(project_sql, 'dict')

        develop_list = []
        req_list = []
        bug_list = []
        project_list = []

        for project in project_dict:

            scale_sql = f"""
                        select b.type, ifnull(a.hour, 0) hour
                        from (
                                 select projectm.fprojectsn project, liaisonf.ftype type, sum(factmanpower) hour
                                 from liaisonf,
                                      projectm
                                 where forganization in {organizations}
                                   and liaisonf.fprojectcd = projectm.fprojectcd
                                   and fcreatedte between date_sub(now(), interval 6 month) and now()
                                   and projectm.fprojectsn = '{project['project']}'
                                 group by project, type) a
                                 right outer join (select distinct ftype type from liaisonf) b on a.type = b.type
                        """

            scale_dict = db_connection_execute(scale_sql, 'dict')
            project_list.append(project['project'])
            for scale in scale_dict:
                if scale['type'] == '追加开发':
                    develop_list.append(scale['hour'])
                elif scale['type'] == '改善需求':
                    req_list.append(scale['hour'])
                else:
                    bug_list.append(scale['hour'])

        data = {}

        data['project'] = project_list
        data['develop'] = develop_list
        data['req'] = req_list
        data['bug'] = bug_list

        return APIResponse(data)


class DashBoardPanelGroup(APIView):

    def get(self, request):
        user = request.user

        project_sql = f"""
                      select count(distinct fodrno) count
                        from liaisonf
                        where fassignedto = '{user.name}'
                           or fleader like '%{user.name}%'
                           or fhelper like '%{user.name}%'
                           or fhelptester = '{user.name}'
                      """

        project_list = query_single_with_no_parameter(project_sql, 'list')

        mcl_sql = f"""
                  select count(*) count
                    from qadf
                    where qahf_id in (select id from qahf where ftesttyp = 'MCL')
                      and fresult in ('OK', 'NGOK', 'NG') and ftestusr = '{user.name}'
                  """

        mcl_list = query_single_with_no_parameter(mcl_sql, 'list')

        pcl_sql = f"""
                  select count(*) count
                    from qadf
                    where qahf_id in (select id from qahf where ftesttyp = 'PCL')
                      and fresult in ('OK', 'NGOK', 'NG') and ftestusr = '{user.name}'
                  """

        pcl_list = query_single_with_no_parameter(pcl_sql, 'list')

        ng_sql = f"""
                 select round(a.count / b.count * 100, 2)
                    from (
                             select count(*) count
                             from qadf
                             where  ftestusr = '{user.name}'
                               and fresult in ('NGOK', 'NG')) a,
                         (select count(*) count
                          from qadf
                          where  ftestusr = '{user.name}'
                            and fresult in ('OK', 'NGOK', 'NG')) b
                 """

        ng_list = query_single_with_no_parameter(ng_sql, 'list')

        data = {}

        data['project'] = project_list[0]
        data['mcl'] = mcl_list[0]
        data['pcl'] = pcl_list[0]
        data['ng'] = ng_list[0]

        return APIResponse(data)


class ProjectBugRateChart(APIView):

    def get(self, request):
        organizations = get_all_organization_group_belong_me(request)
        month_list = []
        project_list = []

        series = []
        series_dict = {}

        month_sql = f"""
                    select distinct date_format(ftestdte, '%Y-%m') month
                        from qahf,
                             liaisonf
                        where liaisonf.forganization in {organizations}
                          and liaisonf.fslipno = qahf.fslipno
                          and qahf.ftestdte between date_sub(now(), interval 6 month) and now()
                    """

        month_dict = db_connection_execute(month_sql, 'dict')

        for month in month_dict:
            month_list.append(month['month'])

        project_sql = f"""
                      select projectm.fprojectcd, fprojectsn
                        from (
                                 select distinct qahf.fprojectcd
                                 from qahf,
                                      liaisonf
                                 where liaisonf.forganization in {organizations}
                                   and liaisonf.fslipno = qahf.fslipno
                                   and date_format(ftestdte, '%Y-%m') in {tuple(month_list)}) a,
                             projectm
                        where a.fprojectcd = projectm.fprojectcd
                      """

        project_dict = db_connection_execute(project_sql, 'dict')

        for project in project_dict:
            ng_list = []
            project_list.append(project['fprojectsn'])
            for month in month_list:
                total_sql = f"""
                            select count(*) count
                                from qadf
                                where qahf_id in (
                                    select qahf.id
                                    from qahf,
                                         liaisonf
                                    where liaisonf.forganization in {organizations}
                                      and liaisonf.fslipno = qahf.fslipno
                                      and date_format(ftestdte, '%Y-%m') = '{month}'
                                      and qahf.fprojectcd = '{project['fprojectcd']}')
                                  and fresult in ('OK', 'NGOK', 'NG')
                            """
                total_dict = db_connection_execute(total_sql, 'dict')

                ng_sql = f"""
                         select count(*) count
                            from qadf
                            where qahf_id in (
                                select qahf.id
                                from qahf,
                                     liaisonf
                                where liaisonf.forganization in {organizations}
                                  and liaisonf.fslipno = qahf.fslipno
                                  and date_format(ftestdte, '%Y-%m') = '{month}'
                                  and qahf.fprojectcd = '{project['fprojectcd']}')
                              and fresult in ('NGOK', 'NG')
                         """

                ng_dict = db_connection_execute(ng_sql, 'dict')

                if total_dict[0]['count'] == 0:
                    ng_rate = 0
                else:
                    ng_rate = ng_dict[0]['count'] / total_dict[0]['count']

                ng_rate = round(ng_rate * 100, 2)

                ng_list.append(ng_rate)

            series_dict['name'] = project['fprojectsn']
            series_dict['data'] = ng_list
            series_dict['type'] = 'line'

            series.append(series_dict)

            series_dict = {}

            data = {}

            data['series'] = series
            data['month'] = month_list
            data['project'] = project_list

        return APIResponse(data)
