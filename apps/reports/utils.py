from django.db.models import Q

from liaisons.models import Liaisons
from qa.models import QaDetail, QaHead


def get_liaison_with_list(slip_no):
    liaison_list = []
    liaison_dict = {}
    liaison = Liaisons.objects.get(fslipno__exact=slip_no)

    liaison_dict['row_1'] = '订单号'
    liaison_dict['row_2'] = liaison.fodrno
    liaison_dict['row_3'] = '系统名称'
    liaison_dict['row_4'] = liaison.fsystemcd
    liaison_dict['row_5'] = '项目名称'
    liaison_dict['row_6'] = liaison.fprojectcd
    liaison_list.append(liaison_dict)
    liaison_dict = {}

    status = '已发布'
    if liaison.fstatus == '1':
        status = '待办'
    if liaison.fstatus == '2':
        status = '已开始'
    if liaison.fstatus == '3':
        status = '已结束'

    liaison_dict['row_1'] = '联络票号'
    liaison_dict['row_2'] = liaison.fslipno
    liaison_dict['row_3'] = '联络票类型'
    liaison_dict['row_4'] = liaison.ftype
    liaison_dict['row_5'] = '状态'
    liaison_dict['row_6'] = status
    liaison_list.append(liaison_dict)
    liaison_dict = {}

    liaison_dict['row_1'] = 'SIR 号'
    liaison_dict['row_2'] = liaison.fsirno
    liaison_dict['row_3'] = '创建日期'
    liaison_dict['row_4'] = str(liaison.fcreatedte)[0:10]
    liaison_dict['row_5'] = '对应者'
    liaison_dict['row_6'] = liaison.fassignedto
    liaison_list.append(liaison_dict)
    liaison_dict = {}

    liaison_dict['row_1'] = '开发概要'
    liaison_dict['row_2'] = liaison.fbrief
    liaison_list.append(liaison_dict)
    liaison_dict = {}

    liaison_dict['row_1'] = '问题描述'
    liaison_dict['row_2'] = liaison.fcontent
    liaison_list.append(liaison_dict)
    liaison_dict = {}

    liaison_dict['row_1'] = '开始日期'
    liaison_dict['row_2'] = liaison.factstart
    liaison_dict['row_3'] = '结束日期'
    liaison_dict['row_4'] = liaison.factend
    liaison_dict['row_5'] = '发布日期'
    liaison_dict['row_6'] = liaison.freleasedt
    liaison_list.append(liaison_dict)
    liaison_dict = {}

    liaison_dict['row_1'] = '测试项目数'
    liaison_dict['row_2'] = QaDetail.objects.filter(Q(fregression__exact='N') &
                                                    ~Q(fresult__in=('CANCEL',)) &
                                                    Q(qahf__fslipno=liaison.fslipno)).count()
    liaison_dict['row_3'] = '回归测试项目数'
    liaison_dict['row_4'] = QaDetail.objects.filter(Q(fregression__exact='Y') &
                                                    ~Q(fresult__in=('CANCEL',)) &
                                                    Q(qahf__fslipno=liaison.fslipno)).count()
    liaison_dict['row_5'] = '问题发生数'
    liaison_dict['row_6'] = QaDetail.objects.filter(Q(fresult__in=('NG', 'NGOK')) &
                                                    Q(qahf__fslipno=liaison.fslipno)).count()
    liaison_list.append(liaison_dict)

    return liaison_list


def get_qa_with_list(slip_no, image):
    qa_head_list = []

    qa_heads = QaHead.objects.filter(fslipno__exact=slip_no)
    for qa_head in qa_heads:
        qa_head_dict = {}
        qa_list = []
        image_list = []

        qa_dict = {}
        qa_dict['row_1'] = '测试对象'
        qa_dict['row_2'] = qa_head.fobjectid
        qa_dict['row_3'] = '确认结果'
        qa_dict['row_4'] = qa_head.freviewcode
        qa_list.append(qa_dict)

        qa_dict = {}
        test_user = qa_head.ftestusr
        if test_user is None:
            test_user = ''
        else:
            test_user = qa_head.ftestusr + ' / ' + str(qa_head.ftestdte)
        auditor = qa_head.fauditor
        if auditor is None:
            auditor = ''
        else:
            auditor = qa_head.fauditor + ' / ' + str(qa_head.fauditdte)
        confirm_user = qa_head.fconfirmusr
        if confirm_user is None:
            confirm_user = ''
        else:
            confirm_user = qa_head.fconfirmusr + ' / ' + str(qa_head.fconfirmdte)

        qa_dict['row_1'] = '测试者/日'
        qa_dict['row_2'] = test_user
        qa_dict['row_3'] = '审核者/日'
        qa_dict['row_4'] = auditor
        qa_dict['row_5'] = '确认者/日'
        qa_dict['row_6'] = confirm_user
        qa_list.append(qa_dict)

        qa_dict = {}
        qa_dict['row_1'] = '回归'
        qa_dict['row_2'] = '测试内容'
        qa_dict['row_3'] = '测试结果'
        qa_dict['row_4'] = '备注'
        qa_list.append(qa_dict)

        qa_details = QaDetail.objects.filter(qahf_id__exact=qa_head.id)

        for qa_detail in qa_details:
            qa_dict = {}

            result = qa_detail.fresult
            if result is None:
                result = ''
            if qa_detail.fcontent_text and len(qa_detail.fcontent_text) > 0:
                result = result + ' / ' + '已贴图'
            regression = '否'
            if qa_detail.fregression == 'Y':
                regression = '是'

            qa_dict['row_1'] = regression
            qa_dict['row_2'] = qa_detail.fcontent
            qa_dict['row_3'] = result
            qa_dict['row_4'] = ''
            qa_list.append(qa_dict)

            if image == 'Y':
                if qa_detail.fcontent_text and len(qa_detail.fcontent_text) > 0:
                    qa_image_dict = {}
                    qa_image_dict['content'] = qa_detail.fcontent
                    qa_image_dict['content_text'] = qa_detail.fcontent_text
                    image_list.append(qa_image_dict)

        qa_head_dict['qa'] = qa_list
        qa_head_dict['image'] = image_list

        qa_head_list.append(qa_head_dict)
    return qa_head_list


def get_qa_content_text_with_list(slip_no):
    qa_image_list = []

    qa_heads = QaHead.objects.filter(fslipno__exact=slip_no)

    qa_details = QaDetail.objects.filter(qahf__in=qa_heads, fcontent_text__isnull=False)

    for qa_detail in qa_details:
        qa_dict = {}

        qa_dict['content'] = qa_detail.fcontent
        qa_dict['content_text'] = qa_detail.fcontent_text

        qa_image_list.append(qa_dict)
    return qa_image_list
