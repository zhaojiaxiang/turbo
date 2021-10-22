from datetime import datetime

from django.db.models import Sum
from suds.client import Client

from qa.models import QaHead, QaDetail
from turbo.settings import env
from utils.db.handler import query_single_with_no_parameter


class SLIMSExchange:
    def __init__(self, request):
        SLIMS = env('SLIMS')
        self.client = Client(SLIMS)
        self.user = request.user

    def insert_slims(self, system_code, project_code, slip_type, slip_no, brief, content, order_no, solution):
        return self.client.service.InsertSlms(datetime.utcnow(), datetime.utcnow(), self.user.slmsname,
                                              self.user.slmsname, project_code, slip_type, slip_no,
                                              system_code, brief, content, order_no, solution)

    def insert_slims_overload(self, instance):
        slip_no = instance.fslipno
        system_code = instance.fsystemcd
        project_code = instance.fprojectcd
        slip_type = instance.ftype
        order_no = instance.fodrno
        brief = instance.fbrief
        content = instance.fcontent
        solution = instance.fsolution

        if slip_type.strip() == "追加开发":
            slip_type = "REQ"
        elif slip_type.strip() == "改善需求":
            slip_type = "EHM"
        else:
            slip_type = "BUG"

        if system_code == "CRUISE":
            system_code = "CMP"

        return self.insert_slims(system_code, project_code, slip_type, slip_no, brief, content, order_no, solution)

    def delete_mcl(self, sir_no, slip_no):
        return self.client.service.DeleteMcl(sir_no, slip_no)

    def fix_slims(self, sir_no, slip_no, total_lines, dev_req_cases, dev_pass_cases, dev_ng_cases):
        ret = self.client.service.FixSlms(sir_no, slip_no, total_lines, 1.0, dev_req_cases, dev_pass_cases,
                                          dev_ng_cases, self.user.slmsname, datetime.utcnow())
        return ret

    def fix_slims_overload(self, sir_no, slip_no):

        total_lines_dict = QaHead.objects.values('fslipno').annotate(total_lines=Sum("fttlcodelines")).filter(
            fslipno__exact=slip_no)

        total_lines = 0
        if total_lines_dict:
            total_lines = total_lines_dict[0]['total_lines']

        sql_str_req = f"select count(*) from qadf where qahf_id in " \
                      f"(select id from qahf where fslipno = '{slip_no}') and fresult <> 'CANCEL'"
        total_dev_cases = query_single_with_no_parameter(sql_str_req, 'list')

        total_dev = total_dev_cases[0]

        # 测试结果为NG的个数，由于存在“评论即NG，在评论NG+1”的功能，因此该结果不能算作NG数量
        sql_str_ng = f"select count(*) from qadf where qahf_id in " \
                     f"(select id from qahf where fslipno = '{slip_no}') and fresult like '%NG%';"
        total_ng_cases = query_single_with_no_parameter(sql_str_ng, 'list')

        total_ng = total_ng_cases[0]

        if total_ng is None:
            total_ng = 0

        # 评论产生NG的总测试项目数
        sql_str_ng_approval = f"select count(*) from qadf where qahf_id in " \
                              f"(select id from qahf where fslipno = '{slip_no}') and fngcnt > 0"

        total_ng_approval_cases = query_single_with_no_parameter(sql_str_ng_approval, 'list')

        total_ng_approval = total_ng_approval_cases[0]

        if total_ng_approval is None:
            total_ng_approval = 0

        # 评论产生的总NG数，一个测试项可能存在多次评论，算作多次NG
        sql_str_ng_approval_sum = f"select sum(fngcnt) from qadf where qahf_id in " \
                                  f"(select id from qahf where fslipno = '{slip_no}')  and fngcnt > 0"

        total_ng_approval_sum_cases = query_single_with_no_parameter(sql_str_ng_approval_sum, 'list')

        total_ng_approval_sum = total_ng_approval_sum_cases[0]

        if total_ng_approval_sum is None:
            total_ng_approval_sum = 0

        ng_count = total_ng + total_ng_approval_sum - total_ng_approval

        ret = self.fix_slims(sir_no, slip_no, total_lines, total_dev, total_dev, ng_count)

        return ret

    def close_slims(self, sir_no):
        ret = self.client.service.CloseSlms(sir_no, self.user.slmsname, datetime.utcnow())

        return ret

    def update_slims(self, sir_no, system_code, project_code, slip_no, slip_type, order_no, brief, content, analyse,
                     solution):
        ret = self.client.service.UpdateSIRF(sir_no, system_code, project_code, slip_no, slip_type, order_no, brief,
                                             content, analyse, solution, self.user.slmsname, datetime.utcnow())
        return ret

    def update_slims_overload(self, validated_data):
        sir_no = validated_data['fsirno']
        slip_no = validated_data['fslipno']
        system_code = validated_data['fsystemcd']
        project_code = validated_data['fprojectcd']
        slip_type = validated_data['ftype']
        order_no = validated_data['fodrno']
        brief = validated_data['fbrief']
        content = validated_data['fcontent']
        analyse = validated_data['fanalyse']
        solution = validated_data['fsolution']

        if slip_type.strip() == "追加开发":
            slip_type = "REQ"
        elif slip_type.strip() == "改善需求":
            slip_type = "EHM"
        else:
            slip_type = "BUG"

        if system_code == "CRUISE":
            system_code = "CMP"

        ret = self.update_slims(sir_no, system_code, project_code, slip_no, slip_type, order_no, brief,
                                content, analyse, solution)
        return ret

    def delete_slims(self, sir_no):
        ret = self.client.service.DeleteSlms(sir_no, self.user.slmsname, datetime.utcnow())
        return ret

    def sync_slims(self, sir_no):
        results = self.client.service.CreateSlipnoBySirno(sir_no)
        return results
