import os
import uuid

from django.db.models import Q
from rest_framework import viewsets
from rest_framework.views import APIView

from accounts.models import User
from accounts.serializers import UserSerializer, MyGroupUserSerializer
from bases import mixins
from bases.response import APIResponse
from liaisons.models import Liaisons
from qa.models import QaHead
from utils.db.handler import db_connection_execute, query_single_with_no_parameter
from utils.handlers.handler import get_all_organization_belong_me, get_all_organization_group_belong_me
from utils.middleware.logger.handler import create_folder


class UpdatePassword(APIView):
    """
    密码修改API
    """

    def post(self, request):
        user = request.user
        old_password = request.data['password']
        new_password = request.data['new_password']

        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return APIResponse()
        else:
            return APIResponse('原始密码不正确')


class UpdateEmailDays(APIView):
    """
    工时系统邮件发送日期修改API
    """

    def post(self, request):
        try:
            user = request.user
            email_days = request.data['email_days']

            user.fmaildays = email_days
            user.save()
        except Exception as ex:
            return APIResponse(ex)
        return APIResponse({"fmaildays": user.fmaildays})


class UpdateAvatar(APIView):
    """
    头像更新API
    """

    def post(self, request):
        try:
            user = request.user

            avatar = request.FILES.get('avatar')

            extension = avatar.name.split('.')[1].lower()

            file_name = "A" + str(uuid.uuid4()) + '.' + extension

            upload_path = "media/avatar"

            create_folder(upload_path)

            file_path = os.path.join(upload_path, file_name)

            with open(file_path, 'wb') as f:
                for i in avatar.chunks():
                    f.write(i)

            avatar_str = "avatar/" + file_name
            user.avatar = avatar_str
            user.save()
        except Exception as ex:
            return APIResponse(ex)
        return APIResponse({"avatar": "http://127.0.0.1:8000/media/" + avatar_str})


class UserListViewSet(mixins.APIListModelMixin, mixins.APIRetrieveModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(is_active=True)


class MyGroupUserViewSet(mixins.APIListModelMixin, mixins.APIRetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = MyGroupUserSerializer

    def get_queryset(self):
        return User.objects.filter(is_active=True, group=self.request.user.group)


class UserDevelopmentDetail(APIView):

    def get(self, request):
        try:
            current_username = request.user.name

            all_not_release_order_sql = f"""
                                       select distinct fodrno, fprojectcd from liaisonf 
                                       where (fassignedto = '{current_username}' or fhelper like '{current_username}' 
                                       or fleader like '{current_username}') and ftype = '追加开发' and fstatus <> 4 """

            all_not_release_orders = db_connection_execute(all_not_release_order_sql)

            response_data = []

            for order in all_not_release_orders:
                order_no = order[0]
                project = order[1]

                order_partner_sql = f"select fassignedto, fleader, fhelper from liaisonf where fodrno = '{order_no}'"
                order_partner_result = db_connection_execute(order_partner_sql)

                user_tuple = ()
                for order_partner_tuple in order_partner_result:
                    user_tuple = user_tuple + order_partner_tuple

                user_list = []
                user_tuple = set(user_tuple)
                for username in user_tuple:
                    if len(username) > 0:
                        if "," in username:
                            split_list = username.split(",")
                            user_list = user_list + split_list
                        else:
                            user_list.append(username)
                user_list = list(set(user_list))
                order_partner = len(user_list)

                order_slipno_all_sql = f"select count(*) from liaisonf where fodrno = '{order_no}'"
                order_slipno_all_list = query_single_with_no_parameter(order_slipno_all_sql, "list")
                order_slipno_all = order_slipno_all_list[0]

                order_slipno_close_sql = f"select count(*) from liaisonf where fodrno = '{order_no}' and fstatus = 3"
                order_slipno_close_list = query_single_with_no_parameter(order_slipno_close_sql, "list")
                order_slipno_close = order_slipno_close_list[0]

                order_slipno_release_sql = f"select count(*) from liaisonf where fodrno = '{order_no}' and fstatus = 4 "
                order_slipno_release_list = query_single_with_no_parameter(order_slipno_release_sql, "list")
                order_slipno_release = order_slipno_release_list[0]

                order_slipno_working_sql = f"select count(*) from liaisonf where fodrno = '{order_no}' and fstatus = 2"
                order_slipno_working_list = query_single_with_no_parameter(order_slipno_working_sql, "list")
                order_slipno_working = order_slipno_working_list[0]

                order_slipno_init_sql = f"select count(*) from liaisonf where fodrno = '{order_no}' and fstatus = 1"
                order_slipno_init_list = query_single_with_no_parameter(order_slipno_init_sql, "list")
                order_slipno_int = order_slipno_init_list[0]

                test_object_sql = f"select count(*) from qahf where fslipno in (select fslipno from liaisonf where fodrno = '{order_no}')"
                test_object_list = query_single_with_no_parameter(test_object_sql, "list")
                test_object = test_object_list[0]

                order_note_sql = f"select fnote from qahf where ftesttyp = 'PCL' and fslipno = '{order_no}'"
                order_note_list = query_single_with_no_parameter(order_note_sql, "list")

                order_note = "******"
                if order_note_list:
                    order_note = order_note_list[0]

                order_status = 1
                if order_slipno_working > 0 or \
                        (
                                order_slipno_working == 0 and order_slipno_close > 0 and order_slipno_close != order_slipno_all):
                    order_status = 2
                elif order_slipno_working == 0 and order_slipno_close == order_slipno_all:
                    order_status = 3
                elif order_slipno_release == order_slipno_all:
                    order_status = 4

                order_dict = {}

                order_dict['order_no'] = order_no
                order_dict['order_note'] = order_note
                order_dict['order_partner'] = order_partner
                order_dict['order_slipno_all'] = order_slipno_all
                order_dict['order_slipno_close'] = order_slipno_close
                order_dict['order_slipno_working'] = order_slipno_working + order_slipno_int
                order_dict['test_object'] = test_object
                order_dict['order_status'] = order_status
                order_dict['project'] = project

                response_data.append(order_dict)
        except Exception as ex:
            return APIResponse(ex)

        return APIResponse(response_data)


class MyTaskBar(APIView):

    def get(self, request):
        try:
            user = request.user

            all_organization_tuple = get_all_organization_belong_me(request)

            all_user = User.objects.values('name').filter(organization__in=all_organization_tuple)

            mcl = QaHead.objects.filter(fcreateusr__exact=user.name,
                                        fstatus__exact='2',
                                        ftesttyp__exact='MCL').count()

            pcl = QaHead.objects.filter(fslipno__in=Liaisons.objects.values('fodrno').
                                        filter(Q(fleader__contains=user.name) |
                                               Q(fassignedto__in=all_user)),
                                        fstatus__in=(1, 2),
                                        ftesttyp__exact='PCL').count()

            all_organization_tuple = get_all_organization_belong_me(request)

            approval_sql = f"""
                           select count(*)
                                from (
                                     select distinct qahf.id  qahf_id,
                                         qahf.ftesttyp,
                                         liaisonf.fodrno,
                                         liaisonf.fslipno,
                                         qahf.fobjectid,
                                         qahf.fstatus,
                                         qahf.fobjmodification,
                                         (select codereview.id
                                          from codereview
                                          where codereview.fobjectid = qahf.fobjectid
                                            and codereview.fslipno = qahf.fslipno) code_id,
                                         (select codereview.id
                                          from codereview
                                          where codereview.fobjectid = 'Design Review'
                                            and codereview.fslipno = qahf.fslipno) design_id
                                     from liaisonf,
                                          qahf,
                                          qadf
                                     where qadf.qahf_id = qahf.id
                                       and (liaisonf.fslipno = qahf.fslipno or liaisonf.fodrno = qahf.fslipno)
                                       and qahf.fcreateusr in (select name from users where organization_id
                                       in {all_organization_tuple})
                                       and qadf.fapproval = 'N'
                                       and qahf.ftesttyp = 'MCL'
                                       and qahf.fstatus in ('1', '2')
                                     union all
                                     select distinct qahf.id,
                                                     qahf.ftesttyp,
                                                     qahf.fslipno,
                                                     qahf.fslipno2 fslipno,
                                                     qahf.fobjectid,
                                                     qahf.fstatus,
                                                     qahf.fnote,
                                                     ''            code_id,
                                                     ''            design_id
                                     from qahf,
                                          qadf,
                                          liaisonf
                                     where ftesttyp = 'PCL'
                                       and qahf.id = qadf.qahf_id
                                       and qadf.fapproval = 'N'
                                       and qahf.fstatus in ('1', '2')
                                       and liaisonf.fodrno = qahf.fslipno
                                       and (liaisonf.fleader like '%{user.name}%' or liaisonf.fassignedto in
                                       (select name from users where organization_id in {all_organization_tuple}))) a
                                order by ftesttyp, fodrno, fslipno
                          """

            approval_list = query_single_with_no_parameter(approval_sql, 'list')
            approval = approval_list[0]
            all_organization_tuple = get_all_organization_belong_me(request)

            confirm_sql = f"""
                          select count(*)
                            from (
                             select qahf.id                                   qahf_id,
                                    qahf.ftesttyp,
                                    liaisonf.fodrno,
                                    liaisonf.fslipno,
                                    qahf.fobjectid,
                                    qahf.fstatus,
                                    qahf.fobjmodification,
                                    (select codereview.id
                                     from codereview
                                     where codereview.fobjectid = qahf.fobjectid
                                       and codereview.fslipno = qahf.fslipno) code_id,
                                    (select codereview.id
                                     from codereview
                                     where codereview.fobjectid = 'Design Review'
                                       and codereview.fslipno = qahf.fslipno) design_id
                             from liaisonf,
                                  qahf
                             where (liaisonf.fslipno = qahf.fslipno or liaisonf.fodrno = qahf.fslipno)
                               and qahf.fcreateusr in (select name from users where organization_id in {all_organization_tuple})
                               and qahf.fstatus = '3'
                               and qahf.ftesttyp = 'MCL'
                             union all
                             select distinct qahf.id,
                                             qahf.ftesttyp,
                                             qahf.fslipno,
                                             qahf.fslipno2 fslipno,
                                             qahf.fobjectid,
                                             qahf.fstatus,
                                             qahf.fnote,
                                             ''            code_id,
                                             ''            design_id
                             from qahf,
                                  liaisonf
                             where qahf.ftesttyp = 'PCL'
                               and qahf.fstatus = '3'
                               and liaisonf.fodrno = qahf.fslipno
                               and (liaisonf.fleader like '%{user.name}%' or liaisonf.fassignedto in
                                (select name from users where organization_id in {all_organization_tuple}))) a1
                          """
            confirm_list = query_single_with_no_parameter(confirm_sql, 'list')
            confirm = confirm_list[0]

            all_organization_group_tuple = get_all_organization_group_belong_me(request)

            dev_count_sql = f"""
                            select count(*)
                                from (
                                     select qahf_c.fslipno, count(*) count
                                     from (
                                          select distinct fslipno, fstatus
                                          from qahf
                                          where fslipno in (
                                              select fslipno
                                              from liaisonf
                                              where fodrno in (
                                                  select fslipno
                                                  from qahf
                                                  where fslipno in (
                                                      select qahf_b.fslipno
                                                      from (select fslipno, count(*) count
                                                            from (select fslipno, fstatus from qahf
                                                            where ftesttyp = 'PCL') qahf_a
                                                            group by fslipno) qahf_b
                                                      where qahf_b.count = 1)
                                                    and fstatus = '4')
                                                and liaisonf.fstatus = '3' and
                                                liaisonf.forganization in {all_organization_group_tuple})) qahf_c
                                     group by qahf_c.fslipno) a
                                where a.count = 1
                            """

            dev_count_list = query_single_with_no_parameter(dev_count_sql, 'list')
            dev_count = dev_count_list[0]

            non_dev_count_sql = f"""
                                select count(*)
                                    from (
                                         select a.fslipno, a.fstatus, count(*) count
                                         from (
                                              select distinct qahf.fslipno, qahf.fstatus
                                              from liaisonf,
                                                   qahf
                                              where liaisonf.fslipno = qahf.fslipno
                                                and liaisonf.ftype <> '追加开发'
                                                and liaisonf.fstatus = '3'
                                                and liaisonf.forganization in {all_organization_group_tuple}) a
                                         group by a.fslipno, a.fstatus) b
                                    where b.count = 1
                                      and b.fstatus = '4';
                                    """

            non_dev_count_list = query_single_with_no_parameter(non_dev_count_sql, 'list')
            non_dev_count = non_dev_count_list[0]

            release = dev_count + non_dev_count

            response_data = []
            task_dict = {}

            task_dict['mcl'] = mcl
            task_dict['pcl'] = pcl
            task_dict['approval'] = approval
            task_dict['confirm'] = confirm
            task_dict['release'] = release

            response_data.append(task_dict)
        except Exception as ex:
            return APIResponse(ex)
        return APIResponse(response_data)


class MyMcl(APIView):

    def get(self, request):
        try:
            user = request.user

            mcl_sql = f"""
                       select
                       liaisonf.id,
                       liaisonf.fslipno,
                       liaisonf.fodrno,
                       (select fnote from qahf where fslipno = liaisonf.fodrno and fslipno2 = 1) fnote,
                       qahf.id qahf_id,
                       trim(qahf.fobjectid) fobjectid,
                       qahf.fsystemcd,
                       qahf.fprojectcd,
                       qahf.fstatus,
                       qahf.ftesttyp,
                       qahf.fcreateusr ftestusr,
                       qahf.fobjmodification,
                       (select codereview.id from codereview where
                            codereview.fobjectid = qahf.fobjectid and codereview.fslipno = qahf.fslipno) code_id,
                       (select codereview.id from codereview where
                            codereview.fobjectid = 'Design Review' and codereview.fslipno = qahf.fslipno) design_id
                       from qahf,
                            liaisonf
                       where qahf.fstatus = '2'
                            and qahf.fcreateusr = '{user.name}'
                            and qahf.ftesttyp = 'MCL'
                            and (liaisonf.fslipno = qahf.fslipno or liaisonf.fodrno = qahf.fslipno)
                       order by liaisonf.fodrno, liaisonf.fslipno
                      """

            mcl_dict = db_connection_execute(mcl_sql, 'dict')
        except Exception as ex:
            return APIResponse(ex)

        return APIResponse(mcl_dict)


class MyPcl(APIView):

    def get(self, request):
        try:
            user = request.user
            all_organization_tuple = get_all_organization_belong_me(request)
            pcl_sql = f"""
                       select distinct qahf.id                                                                     qahf_id,
                            liaisonf.fodrno,
                            qahf.fslipno2                                                               fslipno,
                            qahf.fnote,
                            qahf.fobjectid,
                            qahf.fsystemcd,
                            qahf.fprojectcd,
                            qahf.ftesttyp,
                            qahf.fstatus,
                            (select ifnull(fimpusr, fentusr) from qadf where qahf_id = qahf.id limit 1) ftestusr,
                            ''                                                                          design_id,
                            ''                                                                          code_id
                        from liaisonf,
                             qahf
                        where liaisonf.fodrno = qahf.fslipno
                          and (liaisonf.fleader like '%{user.name}%' or liaisonf.fassignedto in
                              (select name from users where organization_id in {all_organization_tuple}))
                          and qahf.ftesttyp = 'PCL'
                          and qahf.fstatus in (1, 2)
                        order by qahf.fstatus, liaisonf.fodrno
                      """

            pcl_dict = db_connection_execute(pcl_sql, 'dict')
        except Exception as ex:
            return APIResponse(ex)

        return APIResponse(pcl_dict)


class MyApproval(APIView):

    def get(self, request):
        try:
            user = request.user

            all_organization_tuple = get_all_organization_belong_me(request)

            approval_sql = f"""
                           select *
                                from (
                                     select distinct qahf.id  qahf_id,
                                         qahf.ftesttyp,
                                         liaisonf.fodrno,
                                         liaisonf.fslipno,
                                         (select fnote from qahf where fslipno = liaisonf.fodrno and fslipno2 = 1) fnote,
                                         qahf.fobjectid,
                                         qahf.fsystemcd,
                                         qahf.fprojectcd,
                                         qahf.fstatus,
                                         (select ifnull(fimpusr, fentusr) from qadf where qahf_id = qahf.id limit 1) ftestusr,
                                         qahf.fobjmodification,
                                         (select codereview.id
                                          from codereview
                                          where codereview.fobjectid = qahf.fobjectid
                                            and codereview.fslipno = qahf.fslipno) code_id,
                                         (select codereview.id
                                          from codereview
                                          where codereview.fobjectid = 'Design Review'
                                            and codereview.fslipno = qahf.fslipno) design_id
                                     from liaisonf,
                                          qahf,
                                          qadf
                                     where qadf.qahf_id = qahf.id
                                       and (liaisonf.fslipno = qahf.fslipno or liaisonf.fodrno = qahf.fslipno)
                                       and qahf.fcreateusr in (select name from users where organization_id
                                       in {all_organization_tuple})
                                       and qadf.fapproval = 'N'
                                       and qahf.ftesttyp = 'MCL'
                                       and qahf.fstatus in ('1', '2')
                                     union all
                                     select distinct qahf.id,
                                         qahf.ftesttyp,
                                         qahf.fslipno,
                                         qahf.fslipno2 fslipno,
                                         qahf.fnote,
                                         qahf.fobjectid,
                                         qahf.fsystemcd,
                                         qahf.fprojectcd,
                                         qahf.fstatus,
                                         (select ifnull(fimpusr, fentusr) from qadf where qahf_id = qahf.id limit 1) ftestusr,
                                         qahf.fnote,
                                         ''            code_id,
                                         ''            design_id
                                     from qahf,
                                          qadf,
                                          liaisonf
                                     where ftesttyp = 'PCL'
                                       and qahf.id = qadf.qahf_id
                                       and qadf.fapproval = 'N'
                                       and qahf.fstatus in ('1', '2')
                                       and liaisonf.fodrno = qahf.fslipno
                                       and (liaisonf.fleader like '%{user.name}%' or liaisonf.fassignedto in
                                       (select name from users where organization_id in {all_organization_tuple}))) a
                                order by ftesttyp, fodrno, fslipno
                          """

            approval_dict = db_connection_execute(approval_sql, 'dict')
        except Exception as ex:
            return APIResponse(ex)

        return APIResponse(approval_dict)


class MyConfirm(APIView):

    def get(self, request):
        try:
            user = request.user

            all_organization_tuple = get_all_organization_belong_me(request)

            confirm_sql = f"""
                           select qahf.id                                   qahf_id,
                                   qahf.ftesttyp,
                                   liaisonf.fodrno,
                                   liaisonf.fslipno,
                                   (select fnote from qahf where fslipno = liaisonf.fodrno and fslipno2 = 1) fnote,
                                   qahf.fobjectid,
                                   qahf.fsystemcd,
                                   qahf.fprojectcd,
                                   qahf.fstatus,
                                   qahf.ftestusr,
                                   qahf.fobjmodification,
                                   (select codereview.id
                                    from codereview
                                    where codereview.fobjectid = qahf.fobjectid
                                      and codereview.fslipno = qahf.fslipno) code_id,
                                   (select codereview.id
                                    from codereview
                                    where codereview.fobjectid = 'Design Review'
                                      and codereview.fslipno = qahf.fslipno) design_id
                            from liaisonf,
                                 qahf
                            where (liaisonf.fslipno = qahf.fslipno or liaisonf.fodrno = qahf.fslipno)
                              and qahf.fcreateusr in (select name from users where organization_id in {all_organization_tuple})
                              and qahf.fstatus = '3'
                              and qahf.ftesttyp = 'MCL'
                            union all
                            select distinct qahf.id,
                                            qahf.ftesttyp,
                                            qahf.fslipno,
                                            qahf.fslipno2 fslipno,
                                            (select fnote from qahf where fslipno = liaisonf.fodrno and fslipno2 = 1) fnote,
                                            qahf.fobjectid,
                                            qahf.fsystemcd,
                                            qahf.fprojectcd,
                                            qahf.fstatus,
                                            qahf.ftestusr,
                                            qahf.fnote,
                                            ''            code_id,
                                            ''            design_id
                            from qahf,
                                 liaisonf
                            where qahf.ftesttyp = 'PCL'
                              and qahf.fstatus = '3'
                              and liaisonf.fodrno = qahf.fslipno
                              and (liaisonf.fleader like '%{user.name}%' or liaisonf.fassignedto in
                                       (select name from users where organization_id in {all_organization_tuple}))
                          """

            confirm_dict = db_connection_execute(confirm_sql, 'dict')
        except Exception as ex:
            return APIResponse(ex)

        return APIResponse(confirm_dict)


class MyRelease(APIView):

    def get(self, request):
        try:
            all_organization_group_tuple = get_all_organization_group_belong_me(request)

            testing_sql = f"""
                           select *
                                from liaisonf
                                where fslipno in (
                                    select fslipno
                                    from (
                                         select qahf_c.fslipno, count(*) count
                                         from (
                                              select distinct fslipno, fstatus
                                              from qahf
                                              where fslipno in (
                                                  select fslipno
                                                  from liaisonf
                                                  where fodrno in (
                                                      select fslipno
                                                      from qahf
                                                      where fslipno in (
                                                          select qahf_b.fslipno
                                                          from (select fslipno, count(*) count
                                                                from (select fslipno, fstatus from qahf where
                                                                ftesttyp = 'PCL') qahf_a
                                                                group by fslipno) qahf_b
                                                          where qahf_b.count = 1)
                                                        and fstatus = '4')
                                                    and liaisonf.fstatus = '3'
                                                    and liaisonf.forganization in {all_organization_group_tuple})) qahf_c
                                         group by qahf_c.fslipno) a
                                    where a.count = 1
                                    union all
                                    select fslipno
                                    from (
                                         select a.fslipno, a.fstatus, count(*) count
                                         from (
                                              select distinct qahf.fslipno, qahf.fstatus
                                              from liaisonf,
                                                   qahf
                                              where liaisonf.fslipno = qahf.fslipno
                                                and liaisonf.ftype <> '追加开发'
                                                and liaisonf.fstatus = '3'
                                                and liaisonf.forganization in {all_organization_group_tuple}) a
                                         group by a.fslipno, a.fstatus) b
                                    where b.count = 1
                                      and b.fstatus = '4')
                                order by fslipno
                          """

            testing_dict = db_connection_execute(testing_sql, 'dict')
        except Exception as ex:
            return APIResponse(ex)
        return APIResponse(testing_dict)
