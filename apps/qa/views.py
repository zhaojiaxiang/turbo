import datetime
import os
import uuid

from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, filters
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from sendfile import sendfile

from bases.pagination import APIPageNumberPagination
from bases.response import APIResponse
from bases import viewsets, mixins
from checkouts.models import CheckOutFiles
from qa.filters import QaHeadFilter, QaDetailFilter, QaDetailProofFilter, QaSlipNoCheckoutFilter
from qa.models import QaHead, QaDetail, Qadfproof
from qa.serializers import QaHeadSerializer, QaDetailSerializer, QaDetailUpdateResultSerializer, \
    QaDetailUpdateContentTextSerializer, QaHeadUpdateObjectSummarySerializer, QaHeadModifyDetailSerializer, \
    QaHeadTargetAndActualSerializer, PCLQaClass1Serializer, PCLQaClass2Serializer, \
    QaDetailApprovalContentTextSerializer, QadfproofContentTextSerializer, QaSlipNoCheckOutObjectSerializer
from reviews.models import CodeReview
from utils.middleware.logger.handler import create_folder


class MCLQaHeadViewSet(viewsets.APIModelViewSet):
    """
    MCL测试对象增删改查 API
    包含：排序、过滤
    """
    queryset = QaHead.objects.order_by('fstatus', '-fslipno2', '-fcreatedte')
    serializer_class = QaHeadSerializer

    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filter_class = QaHeadFilter

    @transaction.atomic()
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            qa_detail = QaDetail.objects.filter(qahf__exact=instance)
            if instance.fstatus != "1":
                return APIResponse('只有初始状态下才可以删除')
            else:
                if qa_detail:
                    return APIResponse('已经存在测试项不可删除')
                else:
                    if instance.ftesttyp == "PCL":
                        qa_count = QaHead.objects.filter(fslipno__exact=instance.fslipno).count()
                        if qa_count == 1:
                            return APIResponse('已经存在测试项不可删除')
                instance.delete()
            return APIResponse()
        except Exception as ex:
            return APIResponse(ex)


class QaHeadUpdateObjectSummaryViewSet(mixins.APIListModelMixin, mixins.APIRetrieveModelMixin,
                                       mixins.APIUpdateModelMixin, GenericViewSet):
    """
    测试对象 概要 API
    """
    queryset = QaHead.objects.filter(ftesttyp__exact='MCL')
    serializer_class = QaHeadUpdateObjectSummarySerializer


class QaHeadModifyDetailViewSet(mixins.APIListModelMixin, mixins.APIRetrieveModelMixin, mixins.APIUpdateModelMixin,
                                GenericViewSet):
    """
    测试对象 修改明细 API
    """
    queryset = QaHead.objects.filter(ftesttyp__exact='MCL')
    serializer_class = QaHeadModifyDetailSerializer


class QaHeadTargetAndActualViewSet(mixins.APIListModelMixin, mixins.APIRetrieveModelMixin, GenericViewSet):
    """
    测试对象 测试目标 API
    """
    queryset = QaHead.objects.all()
    serializer_class = QaHeadTargetAndActualSerializer


class QaDetailViewSet(viewsets.APIModelViewSet):
    """
    测试明细表 增删改查 API
    """
    queryset = QaDetail.objects.all().order_by('fsortrule', 'fclass1', 'fclass2', 'fregression', '-pk')
    serializer_class = QaDetailSerializer

    pagination_class = APIPageNumberPagination

    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filter_class = QaDetailFilter


class BatchNewQaDetail(APIView):

    @transaction.atomic()
    def post(self, request):
        try:
            user = request.user
            batch_data = request.data['data']

            special_symbols = ('+', ' ', '/', '?', '%', '#', '&', '=')

            batch_qa = []
            for qa in batch_data:

                for symbol in special_symbols:
                    if symbol in qa['fclass1']:
                        return APIResponse(f'分类1中不可包含特殊符号{symbol}')
                    if symbol in qa['fclass2']:
                        return APIResponse(f'分类2中不可包含特殊符号{symbol}')
                batch_qa.append(
                    QaDetail(fclass1=qa['fclass1'], fclass2=qa['fclass2'], fregression=qa['fregression'],
                             fcontent=qa['fcontent'], fsortrule=qa['fsortrule'], qahf_id=qa['qahf'], fimpusr=user.name,
                             fentusr=user.name, fupdteprg='QA Batch New'))

            QaDetail.objects.bulk_create(batch_qa)
            return APIResponse()
        except Exception as ex:
            return APIResponse(ex)


class QaDetailUpdateResultViewSet(mixins.APIListModelMixin, mixins.APIRetrieveModelMixin, mixins.APIUpdateModelMixin,
                                  viewsets.GenericViewSet):
    """
    测试项结果 更新修改查看 API
    """
    queryset = QaDetail.objects.all()
    serializer_class = QaDetailUpdateResultSerializer


class QaDetailUpdateContentTextViewSet(mixins.APIListModelMixin, mixins.APIRetrieveModelMixin,
                                       mixins.APIUpdateModelMixin,
                                       GenericViewSet):
    """
    测试项贴图 更新修改查看 API
    """
    queryset = QaDetail.objects.all()
    serializer_class = QaDetailUpdateContentTextSerializer


class QaDetailApprovalContentTextViewSet(mixins.APIListModelMixin, mixins.APIRetrieveModelMixin,
                                         mixins.APIUpdateModelMixin, GenericViewSet):
    """
    测试项评论贴图，提交测试结果后，检查测试项时评论功能 更新修改查看 API
    """
    queryset = QaDetail.objects.all()
    serializer_class = QaDetailApprovalContentTextSerializer


class QadfProofContentTextViewSet(mixins.APIListModelMixin, mixins.APIRetrieveModelMixin, GenericViewSet):
    """

    """
    queryset = Qadfproof.objects.all().order_by('-id')
    serializer_class = QadfproofContentTextSerializer

    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filter_class = QaDetailProofFilter


class PCLQaClass1ViewSet(mixins.APIListModelMixin, mixins.APIRetrieveModelMixin, GenericViewSet):
    """
    PCL 以分类1进行分组展示数据 API
    """
    queryset = QaHead.objects.filter(ftesttyp__exact='PCL')
    serializer_class = PCLQaClass1Serializer


class PCLQaClass2ViewSet(mixins.APIListModelMixin, mixins.APIRetrieveModelMixin, GenericViewSet):
    """
    PCL 以分类1 + 分类2进行分组展示数据 API
    """
    serializer_class = PCLQaClass2Serializer

    def get_queryset(self):
        qahf = self.request.GET.get('qahf_id')
        class1 = self.request.GET.get('class1')
        queryset = QaDetail.objects.filter(qahf_id__exact=qahf, fclass1__exact=class1).values('qahf_id',
                                                                                              'fclass1').distinct()
        return queryset


class QaSlipNoCheckOutObject(mixins.APIListModelMixin, mixins.APIRetrieveModelMixin, GenericViewSet):
    serializer_class = QaSlipNoCheckOutObjectSerializer
    queryset = CheckOutFiles.objects.values('fchkoutobj').all()

    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filter_class = QaSlipNoCheckoutFilter


class PCLCommitJudgment(APIView):

    def get(self, request):
        try:
            qahf_id = request.GET.get('qahf')
            qahead = QaHead.objects.filter(pk=qahf_id)
            qa_status = qahead[0].fstatus
            qa_result = 'OK'
            qadetail = QaDetail.objects.filter(qahf_id__exact=qahf_id).values('fresult').distinct()
            for qa in qadetail:
                if qa['fresult'] == 'NG':
                    qa_result = 'NG'
                    break
                elif qa['fresult'] is None:
                    qa_result = 'NG'
                    break

            data = {'status': qa_status, 'result': qa_result}
            return APIResponse(data)
        except Exception as ex:
            return APIResponse(ex)


class TestResultDefaultOK(APIView):
    """
    MCL和PCL列表中，点击Default OK按钮，将该测试对象下所有未录入结果的测试项默认设置为 “OK”
    """

    @transaction.atomic()
    def put(self, request):
        user = request.user
        try:
            qahf_id = request.data['qahf']
            qa_details = QaDetail.objects.filter(qahf_id=qahf_id)
            for detail in qa_details:
                if detail.fresult is None:
                    detail.fresult = 'OK'
                    detail.ftestusr = user.name
                    detail.ftestdte = datetime.datetime.now().strftime('%Y-%m-%d')
                    detail.save()
            return APIResponse()
        except Exception as ex:
            return APIResponse(ex)


class CodeReviewInspection(APIView):

    def get(self, request):
        object_id = request.GET.get('object_id')
        slip_no = request.GET.get('slip_no')

        code_review = CodeReview.objects.filter(fobjectid__exact=object_id,
                                                fslipno__exact=slip_no)
        if code_review.count() == 0:
            return APIResponse('代码Review没填写')
        return APIResponse()


@permission_classes((AllowAny,))
class RecoverFile(APIView):
    """
    富文本编辑器文件展示处理API
    """

    def get(self, request, filename):
        ret_url = os.path.join("media/upload/image", filename[0], filename[1], filename)

        return sendfile(request, filename=ret_url, attachment=True)


class CkEditorImageUpload(APIView):
    """
    富文本编辑器图片上传API
    """

    def post(self, request):
        try:
            image = request.FILES.get('file')

            extension = image.name.split('.')[1].lower()

            image_name = str(uuid.uuid4()) + '.' + extension

            upload_path = os.path.join("media/upload/image", image_name[0], image_name[1])

            create_folder(upload_path)

            image_save_path = os.path.join(upload_path, image_name)

            # 保存单个文件
            with open(image_save_path, 'wb') as f:
                for i in image.chunks():
                    f.write(i)

            ret_url = os.path.join("files", image_name)

            data = {"code": 0, "msg": "success", "data": {"url": ret_url}}
            return APIResponse(data)
        except Exception as ex:
            return APIResponse(ex)


@permission_classes((AllowAny,))
class CkEditorFileUpload(APIView):
    """
    富文本编辑器文件上传API
    """

    def post(self, request):
        try:
            orig_file = request.FILES.get('file')

            extension = orig_file.name.split('.')[1].lower()

            file_name = "T" + str(uuid.uuid4()) + '.' + extension

            upload_path = os.path.join("media/upload/image", file_name[0], file_name[1])

            create_folder(upload_path)

            file_path = os.path.join(upload_path, file_name)

            # file_path
            with open(file_path, 'wb') as f:
                for i in orig_file.chunks():
                    f.write(i)

            ret_url = os.path.join('files', file_name)

            ret_path = f'<p><a href="{ret_url}">{orig_file}</a></p>'

            data = {"path": ret_path}

            return APIResponse(data)
        except Exception as ex:
            return APIResponse(ex)


class JudgeTestTypeByQaDetail(APIView):

    def get(self, request):

        qadf = request.GET.get('qadf')

        qadf = QaDetail.objects.get(id=qadf)

        data = {'id': qadf.qahf.id, 'type': qadf.qahf.ftesttyp, 'class1': qadf.fclass1, 'class2': qadf.fclass2}
        return APIResponse(data)
