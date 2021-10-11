import datetime
from decimal import Decimal

from django.db import transaction
from django.db.models import Max, Q, Sum
from math import ceil
from rest_framework import serializers

from checkouts.models import CheckOutFiles
from liaisons.models import Liaisons
from qa.models import QaHead, QaDetail, Qadfproof
from reviews.models import CodeReview


class QaHeadSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    fcreatedte = serializers.DateTimeField(read_only=True)
    fcreateusr = serializers.CharField(read_only=True)
    ftestdte = serializers.DateField(read_only=True)
    ftestusr = serializers.CharField(read_only=True)
    fconfirmdte = serializers.DateField(read_only=True)
    fconfirmusr = serializers.CharField(read_only=True)
    fauditdte = serializers.DateField(read_only=True)
    fauditor = serializers.CharField(read_only=True)
    fslipno2 = serializers.IntegerField(read_only=True)

    qadfcount = serializers.SerializerMethodField()

    class Meta:
        model = QaHead
        fields = ('id', 'fsystemcd', 'fprojectcd', 'fslipno', 'fslipno2', 'fobjectid', 'fobjmodification',
                  'fcreatedte', 'fcreateusr', 'ftestusr', 'fstatus', 'ftesttyp', 'qadfcount', 'freviewcode', 'flevel',
                  'ftestdte', 'ftestusr', 'fconfirmdte', 'fconfirmusr', 'fauditdte', 'fauditor')

    def get_qadfcount(self, obj):
        qadf = QaDetail.objects.filter(qahf_id__exact=obj.id)
        return qadf.count()

    @transaction.atomic()
    def create(self, validated_data):

        test_type = validated_data['ftesttyp']
        slip_no2 = 1
        if test_type == 'MCL':
            is_exist = QaHead.objects.filter(fslipno__exact=validated_data['fslipno'],
                                             fobjectid__exact=validated_data['fobjectid'])

            if is_exist.count() > 0:
                raise serializers.ValidationError("该测试对象已经在该联络下存在")
        else:
            is_order_exist = Liaisons.objects.filter(fodrno__exact=validated_data['fslipno'])
            if is_order_exist.count() == 0:
                raise serializers.ValidationError("该订单在系统中不存在")
            max_slipno2 = QaHead.objects.filter(fslipno__exact=validated_data['fslipno']).aggregate(Max('fslipno2'))
            if max_slipno2['fslipno2__max']:
                slip_no2 = max_slipno2['fslipno2__max'] + 1
            else:
                slip_no2 = 1

        user = self.context['request'].user
        qahead = QaHead.objects.create(**validated_data)
        qahead.ftesttyp = test_type
        qahead.fobjectnm = validated_data['fobjectid']
        qahead.fcreateusr = user.name
        qahead.fslipno2 = slip_no2
        qahead.fstatus = '1'
        qahead.fentusr = user.name
        qahead.fupdteprg = 'QA New'
        qahead.save()
        return qahead

    @transaction.atomic()
    def update(self, instance, validated_data):
        qa_details = QaDetail.objects.filter(qahf__exact=instance)
        orig_status = instance.fstatus
        new_status = validated_data['fstatus']
        user = self.context['request'].user

        diff_status = int(new_status) - int(orig_status)
        if abs(diff_status) > 1:
            raise serializers.ValidationError("测试对象状态不可跨级修改，系统流程控制Bug！")

        if diff_status > 0:
            if new_status == '2':
                """审核"""
                if qa_details.count() == 0:
                    raise serializers.ValidationError("测试明细为空，不可审核")

                lot = instance.flastapprovallot + 1
                instance.fstatus = new_status
                instance.fauditdte = datetime.datetime.now().strftime('%Y-%m-%d')
                instance.flastapprovallot = lot
                instance.fauditor = user.name
                instance.fupdteusr = user.name
                instance.fupdteprg = "QA Approval"
                instance.save()

                for qa in qa_details:
                    if qa.fapproval != "Y":
                        qa.fapproval = "Y"
                        qa.fapprovallot = lot
                        qa.fupdteusr = user.name
                        qa.fupdteprg = "QA Approval"
                        qa.save()

            if new_status == '3':
                """测试结果提交"""
                for qa in qa_details:
                    if qa.fresult == 'NG':
                        raise serializers.ValidationError("存在未处理NG项，不可提交")
                if instance.ftesttyp == "MCL":
                    if instance.fobjmodification is None:
                        raise serializers.ValidationError("请先填写测试对象修改概要")

                    if instance.fcomplexity is None:
                        raise serializers.ValidationError("请先填写修改明细")

                    if instance.fttlcodelines is None:
                        raise serializers.ValidationError("请先填写修改明细")

                    # code_review = CodeReview.objects.filter(fobjectid__exact=instance.fobjectid,
                    #                                         fslipno__exact=instance.fslipno)
                    # if code_review.count() == 0:
                    #     raise serializers.ValidationError("请先填写代码Review")

                    liaison = Liaisons.objects.filter(fslipno__exact=instance.fslipno)
                    if liaison[0].ftype == "追加开发":
                        design_review = CodeReview.objects.filter(fobjectid__exact="Design Review",
                                                                  fslipno__exact=instance.fslipno)
                        if design_review.count() == 0:
                            raise serializers.ValidationError("请先填写设计Review")

                instance.fstatus = new_status
                instance.ftestdte = datetime.datetime.now().strftime('%Y-%m-%d')
                instance.ftestusr = user.name
                instance.fupdteusr = user.name
                instance.fupdteprg = "QA Submit"
                instance.save()

            if new_status == '4':
                """确认"""

                if instance.ftesttyp == "MCL":
                    code_review = CodeReview.objects.filter(fobjectid__exact=instance.fobjectid,
                                                            fslipno__exact=instance.fslipno)
                    if code_review.count() == 0:
                        raise serializers.ValidationError("请先填写代码Review")

                for qa in qa_details:
                    if qa.fresult == 'NG':
                        raise serializers.ValidationError("存在未处理NG项，不可确认")

                instance.fstatus = new_status
                instance.fconfirmdte = datetime.datetime.now().strftime('%Y-%m-%d')
                instance.flevel = validated_data['flevel']
                instance.freviewcode = validated_data['freviewcode']
                instance.fconfirmusr = user.name
                instance.fupdteusr = user.name
                instance.fupdteprg = "QA Confirm"
                instance.save()
        elif diff_status < 0:
            if new_status == '3':
                """取消确认"""
                instance.fstatus = new_status
                instance.fconfirmdte = None
                instance.fconfirmusr = ""
                instance.flevel = ''
                instance.freviewcode = ''
                instance.fupdteusr = user.name
                instance.fupdteprg = "QA Confirm Cancel"
                instance.save()

            if new_status == '2':
                """取消结果提交"""
                instance.fstatus = new_status
                instance.ftestdte = None
                instance.ftestusr = ""
                instance.fupdteusr = user.name
                instance.fupdteprg = "QA Submit Cancel"
                instance.save()

            if new_status == '1':
                """审核审核， 该逻辑原则上不会出现"""
                lot = instance.flastapprovallot - 1
                instance.fstatus = new_status
                instance.fauditdte = None
                instance.fauditor = ""
                instance.flastapprovallot = lot
                instance.fupdteusr = user.name
                instance.fupdteprg = "QA Approval Cancel"
                instance.save()

                for qa in qa_details:
                    qa.fapproval = "N"
                    qa.fupdteusr = user.name
                    qa.fapprovallot = qa.fapprovallot - 1
                    qa.fupdteprg = "QA Approval Cancel"
                    qa.save()
        else:
            if new_status == '2':
                """审核"""
                lot = instance.flastapprovallot + 1
                instance.fstatus = new_status
                instance.fauditdte = datetime.datetime.now().strftime('%Y-%m-%d')
                instance.flastapprovallot = lot
                instance.fauditor = user.name
                instance.fupdteusr = user.name
                instance.fupdteprg = "QA Approval"
                instance.save()

                for qa in qa_details:
                    if qa.fapproval != "Y":
                        qa.fapproval = "Y"
                        qa.fapprovallot = lot
                        qa.fupdteusr = user.name
                        qa.fupdteprg = "QA Approval"
                        qa.save()

            if new_status == '1':
                instance.fobjectid = validated_data['fobjectid']
                instance.fobjectnm = validated_data['fobjectid']
                instance.fupdteusr = user.name
                instance.fupdteprg = "QA Head Modify"
                instance.save()

        return instance


class QaHeadDisplayNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = QaHead
        fields = ('fnote',)


class QaHeadUpdateObjectSummarySerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)

    class Meta:
        model = QaHead
        fields = ('id', 'fobjmodification')


class QaHeadModifyDetailSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)

    class Meta:
        model = QaHead
        fields = ('id', 'fttlcodelines', 'fmodifiedlines', 'fcomplexity', 'fselflevel', 'fstatus', 'ftargettest',
                  'ftargetregtest', 'ftargetng')


class QaSlipNoCheckOutObjectSerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField()

    class Meta:
        model = CheckOutFiles
        fields = ('value', 'fchkoutobj')

    def get_value(self, obj):
        return obj['fchkoutobj']


class PCLQaClass1Serializer(serializers.ModelSerializer):
    class1 = serializers.SerializerMethodField()

    class Meta:
        model = QaHead
        fields = ('id', 'class1')

    def get_class1(self, obj):
        qadetail = QaDetail.objects.filter(qahf_id__exact=obj.id).values('fclass1').distinct()
        for class1 in qadetail:
            class2 = QaDetail.objects.filter(qahf_id__exact=obj.id, fclass1__exact=class1['fclass1']).values(
                'fclass2').distinct()

            class1['class2_cnt'] = class2.count()

            mcl = QaDetail.objects.filter(qahf_id__exact=obj.id, fclass1__exact=class1['fclass1'])

            class1['test_cnt'] = mcl.count()

            qahead = QaHead.objects.filter(pk=obj.id)
            class1['status'] = qahead[0].fstatus

            tested_mcl = QaDetail.objects.filter(qahf_id__exact=obj.id, fclass1__exact=class1['fclass1'],
                                                 fresult__in=('NG', 'NGOK', 'OK'))

            class1['tested_cnt'] = tested_mcl.count()

            canceled_mcl = QaDetail.objects.filter(qahf_id__exact=obj.id, fclass1__exact=class1['fclass1'],
                                                   fresult__exact='CANCEL')

            class1['canceled_cnt'] = canceled_mcl.count()

            class1['ng'] = QaDetail.objects.filter(qahf_id__exact=obj.id, fclass1__exact=class1['fclass1'],
                                                   fresult__exact='NG').count()

        return qadetail


class PCLQaClass2Serializer(serializers.ModelSerializer):
    class2 = serializers.SerializerMethodField()

    class Meta:
        model = QaDetail
        fields = ('fclass1', 'class2')

    def get_class2(self, obj):
        class1 = self.context['request'].GET.get('class1')
        qahf = self.context['request'].GET.get('qahf_id')
        qadetail = QaDetail.objects.filter(qahf_id__exact=qahf, fclass1__exact=class1).values('fclass2').distinct()

        for class2 in qadetail:
            mcl = QaDetail.objects.filter(qahf_id__exact=qahf, fclass1__exact=class1, fclass2__exact=class2['fclass2'])
            class2['test_cnt'] = mcl.count()

            qahead = QaHead.objects.filter(pk=qahf)
            class2['status'] = qahead[0].fstatus

            tested_mcl = QaDetail.objects.filter(qahf_id__exact=qahf, fclass1__exact=class1,
                                                 fclass2__exact=class2['fclass2'],
                                                 fresult__in=('NG', 'NGOK', 'OK'))

            class2['tested_cnt'] = tested_mcl.count()

            canceled_mcl = QaDetail.objects.filter(qahf_id__exact=qahf, fclass1__exact=class1,
                                                   fclass2__exact=class2['fclass2'],
                                                   fresult__exact='CANCEL')

            class2['canceled_cnt'] = canceled_mcl.count()

            class2['ng'] = QaDetail.objects.filter(qahf_id__exact=qahf, fclass1__exact=class1,
                                                   fclass2__exact=class2['fclass2'], fresult__exact='NG').count()

        return qadetail


class QaHeadTargetAndActualSerializer(serializers.ModelSerializer):
    target_tests = serializers.SerializerMethodField()
    target_regressions = serializers.SerializerMethodField()
    target_total = serializers.SerializerMethodField()
    target_ng = serializers.SerializerMethodField()
    actual_tests = serializers.SerializerMethodField()
    actual_regressions = serializers.SerializerMethodField()
    actual_total = serializers.SerializerMethodField()
    actual_ng = serializers.SerializerMethodField()
    actual_ngok = serializers.SerializerMethodField()
    actual_ng_rate = serializers.SerializerMethodField()

    class Meta:
        model = QaHead
        fields = (
            'id', 'fttlcodelines', 'fmodifiedlines', 'fcomplexity', 'fstatus', 'target_tests', 'target_regressions',
            'target_total', 'target_ng', 'actual_tests', 'actual_regressions', 'actual_total', 'actual_ng',
            'actual_ngok', 'actual_ng_rate')

    def get_target_tests(self, obj):
        if obj.ftargettest:
            return obj.ftargettest
        if obj.fmodifiedlines:
            return ceil(obj.fmodifiedlines * obj.fcomplexity / 11)
        return 0

    def get_target_regressions(self, obj):
        if obj.ftargetregtest:
            return obj.ftargetregtest
        if obj.fttlcodelines:
            return ceil(obj.fttlcodelines / 50)
        return 0

    def get_target_total(self, obj):
        if obj.ftargettest:
            return self.get_target_regressions(obj) + self.get_target_tests(obj)
        if obj.fttlcodelines:
            return self.get_target_regressions(obj) + self.get_target_tests(obj)
        return 0

    def get_target_ng(self, obj):
        if obj.ftargetng:
            return obj.ftargetng
        if obj.fmodifiedlines:
            return ceil(self.get_target_tests(obj) / 11)
        return 0

    def get_actual_tests(self, obj):
        return QaDetail.objects.filter(fregression__exact='N',
                                       fresult__in=('OK', 'NG', 'NGOK',),
                                       qahf_id__exact=obj.id).count()

    def get_actual_regressions(self, obj):
        return QaDetail.objects.filter(fregression__exact='Y',
                                       fresult__in=('OK', 'NG', 'NGOK',),
                                       qahf_id__exact=obj.id).count()

    def get_actual_total(self, obj):
        return QaDetail.objects.filter(fresult__in=('OK', 'NG', 'NGOK',),
                                       qahf_id__exact=obj.id).count()

    def get_actual_ng(self, obj):
        # 测试结果为NG的数量, 可以参考slims.py文件中的fix_slims_overload方法
        result_ng_count = QaDetail.objects.filter(fresult__contains='NG',
                                                  qahf_id__exact=obj.id).count()
        approval_ng_count = QaDetail.objects.filter(fresult__contains='NG',
                                                    qahf_id__exact=obj.id, fngcnt__gt=0).count()
        approval_ng_sum_dict = QaDetail.objects.values('qahf_id').annotate(sum=Sum("fngcnt")).filter(
            fresult__contains='NG', qahf_id__exact=obj.id, fngcnt__gt=0)

        approval_ng_sum = 0
        if approval_ng_sum_dict:
            approval_ng_sum = approval_ng_sum_dict[0]['sum']

        return result_ng_count + approval_ng_sum - approval_ng_count

    def get_actual_ngok(self, obj):
        result_ngok_count = QaDetail.objects.filter(fresult__exact='NGOK',
                                                    qahf_id__exact=obj.id).count()
        return result_ngok_count

    def get_actual_ng_rate(self, obj):

        total = self.get_actual_total(obj)
        if total == 0:
            total = 1
        ng_rate = round(Decimal(self.get_actual_ng(obj) / total * 100), 2)

        return str(ng_rate) + "%"


class QaDetailSerializer(serializers.ModelSerializer):
    # qahf = QaHeadSerializer()  # 获取反向获取外键的相关字段

    id = serializers.IntegerField(read_only=True)
    fimpdte = serializers.DateField(read_only=True)
    fimpusr = serializers.DateField(read_only=True)
    ftestdte = serializers.DateField(read_only=True)
    ftestusr = serializers.CharField(read_only=True)
    fapproval = serializers.CharField(read_only=True)
    fngcnt = serializers.IntegerField(read_only=True)
    fresult = serializers.CharField(read_only=True)
    fcontent_text = serializers.CharField(read_only=True)
    test_tag = serializers.SerializerMethodField()

    class Meta:
        model = QaDetail
        fields = ('id', 'fclass1', 'fclass2', 'fregression', 'fcontent', 'fsortrule', 'fimpdte', 'fimpusr', 'ftestdte',
                  'ftestusr', 'fapproval', 'fresult', 'fngcnt', 'qahf', 'fapproval', 'fcontent_text', 'test_tag')

    def get_test_tag(self, obj):
        context_text = obj.fcontent_text
        ng_cnt = obj.fngcnt
        last_submit = obj.flastsubmitid
        last_approval = obj.flastapproveid

        if context_text and len(context_text) > 0:
            if ng_cnt == 0:
                return "已贴图"
            else:
                if last_approval > last_submit:
                    return f"已评论,{ng_cnt}"
                else:
                    return f"已贴图,{ng_cnt}"
        else:
            if ng_cnt > 0:
                return f"已评论,{ng_cnt}"
            return "贴图"

    @transaction.atomic()
    def create(self, validated_data):
        # is_exist = QaDetail.objects.filter(Q(fcontent__exact=validated_data['fcontent']),
        #                                    Q(qahf_id__exact=validated_data['qahf']) & ~Q(fresult__exact='CANCEL'))
        # if is_exist.count() > 0:
        #     raise serializers.ValidationError("该测试项已经在该对象下存在")
        try:
            user = self.context['request'].user
            qadetail = QaDetail.objects.create(**validated_data)
            qadetail.fimpusr = user.name
            qadetail.fentusr = user.name
            qadetail.fupdteprg = "QA New"
            qadetail.save()
            return qadetail
        except Exception as ex:
            raise serializers.ValidationError(ex.args[0])

    @transaction.atomic()
    def update(self, instance, validated_data):
        approval = instance.fapproval
        result = instance.fresult

        if approval == "Y":
            raise serializers.ValidationError('已经审核的测试项不可修改')
        else:
            if result:
                raise serializers.ValidationError('存在测试结果的测试项不可修改')
        return super().update(instance, validated_data)


class QaDetailUpdateResultSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = QaDetail
        fields = ('id', 'fresult')

    @transaction.atomic()
    def update(self, instance, validated_data):
        user = self.context['request'].user
        result_original = instance.fresult
        result_present = validated_data['fresult']

        # if result_original:
        #     if "NG" in result_original and result_present == "OK":
        #         raise serializers.ValidationError("测试结果不可由NG修改为OK！！！")
        #
        #     if result_original == "CANCEL":
        #         raise serializers.ValidationError("已经取消的测试项不可修改")

        instance.fresult = result_present
        instance.ftestusr = user.name
        instance.ftestdte = datetime.datetime.now().strftime('%Y-%m-%d')
        instance.save()
        return instance


class QaDetailUpdateContentTextSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    status = serializers.SerializerMethodField()

    class Meta:
        model = QaDetail
        fields = ('id', 'status', 'fcontent', 'fcontent_text')

    def get_status(self, obj):
        return obj.qahf.fstatus

    @transaction.atomic()
    def update(self, instance, validated_data):
        user = self.context['request'].user
        fcontent_text = validated_data['fcontent_text']
        qadf_id = instance.id
        fentusr = user.name

        proof_data = {"fcontent_text": fcontent_text, "fentusr": fentusr, "qadf_id": qadf_id}

        proof_id = 0
        if instance.flastapproveid is None:

            if instance.flastsubmitid:
                proof_id = instance.flastsubmitid
                proof = Qadfproof.objects.get(pk=proof_id)
                proof.fcontent_text = fcontent_text
            else:
                proof = Qadfproof.objects.create(**proof_data)
                proof_id = proof.id
            proof.save()
        else:
            if instance.flastsubmitid is None or instance.flastapproveid > instance.flastsubmitid:
                proof = Qadfproof.objects.create(**proof_data)
                proof_id = proof.id
                proof.save()
            else:
                proof_id = instance.flastsubmitid
                proof_data['id'] = proof_id
                proof = Qadfproof.objects.get(pk=proof_id)
                proof.fcontent_text = fcontent_text
                proof.save()

        instance.flastsubmitid = proof_id
        instance.fcontent_text = fcontent_text
        instance.ftestusr = user.name
        instance.ftestdte = datetime.datetime.now().strftime('%Y-%m-%d')
        instance.save()

        return instance


class QaDetailApprovalContentTextSerializer(serializers.ModelSerializer):
    """
    处理测试项评论
    """
    id = serializers.IntegerField(read_only=True)
    status = serializers.SerializerMethodField()

    class Meta:
        model = QaDetail
        fields = ('id', 'status', 'fcontent', 'fcontent_text')

    def get_status(self, obj):
        return obj.qahf.fstatus

    @transaction.atomic()
    def update(self, instance, validated_data):
        user = self.context['request'].user
        fcontent_text = validated_data['fcontent_text']
        qadf_id = instance.id
        fentusr = user.name

        proof_data = {"fcontent_text": fcontent_text, "fentusr": fentusr, "qadf_id": qadf_id}

        proof_id = 0
        ng_count = instance.fngcnt
        result = instance.fresult
        if instance.flastapproveid is None:
            proof = Qadfproof.objects.create(**proof_data)
            proof_id = proof.id
            proof.save()
            ng_count = ng_count + 1
            result = "NG"
        else:
            if instance.flastsubmitid > instance.flastapproveid:
                proof = Qadfproof.objects.create(**proof_data)
                proof_id = proof.id
                proof.save()
                ng_count = ng_count + 1
                result = "NG"
            else:
                proof_id = instance.flastapproveid
                proof = Qadfproof.objects.get(pk=proof_id)
                proof.fcontent_text = fcontent_text
                proof.save()

        instance.flastapproveid = proof_id
        instance.fresult = result
        instance.fngcnt = ng_count
        instance.save()

        return instance


class QadfproofContentTextSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    user_date_tag = serializers.SerializerMethodField()

    class Meta:
        model = Qadfproof
        fields = ('id', 'qadf_id', 'fcontent_text', 'fentdt', 'fentusr', 'type', 'user_date_tag')

    def get_user_date_tag(self, obj):
        return obj.fentusr + " - " + str(obj.fentdt)

    def get_type(self, obj):
        qa_detail = QaDetail.objects.get(pk=obj.qadf_id)
        last_approval = qa_detail.flastapproveid
        last_submit = qa_detail.flastsubmitid

        proof_type = "H"
        """
        H: 历史测试、评论数据
        A: 最新的评论
        T: 最新的测试数据
        """
        if last_approval == obj.id:
            proof_type = "A"
        if last_submit == obj.id:
            proof_type = "T"

        return proof_type
