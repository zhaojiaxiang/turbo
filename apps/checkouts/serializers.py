import datetime

from django.db import transaction
from rest_framework import serializers

from checkouts.models import CheckOutFiles


class CheckOutFilesSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    fregisterdte = serializers.DateField(read_only=True)
    fapplicant = serializers.CharField(read_only=True)
    fchkoutperson = serializers.CharField(read_only=True)
    fchkoutdte = serializers.DateField(read_only=True)
    fchkinperson = serializers.CharField(read_only=True)
    fchkindte = serializers.DateField(read_only=True)

    class Meta:
        model = CheckOutFiles
        fields = ('id', 'fsystem', 'fcomment', 'fslipno', 'fchkoutobj', 'fchkoutfile', 'fchkstatus', 'fregisterdte',
                  'fapplicant', 'fchkoutperson', 'fchkoutdte', 'fchkinperson', 'fchkindte')

    @transaction.atomic()
    def create(self, validated_data):
        user = self.context['request'].user

        system = validated_data['fsystem']
        chkoutobj = validated_data['fchkoutobj']
        comment = validated_data['fcomment']

        ask_status = ('2-Check Out', '1-ASK')

        files = CheckOutFiles.objects.filter(fsystem__exact=system, fchkoutobj__exact=chkoutobj, fcomment=comment,
                                             fchkstatus__in=ask_status)

        if files.count() > 0:
            raise serializers.ValidationError("该对象已经迁出")

        checkoutfile = CheckOutFiles.objects.create(**validated_data)
        checkoutfile.fapplicant = user.name
        checkoutfile.applicant = user
        checkoutfile.save()

        return checkoutfile

    @transaction.atomic()
    def update(self, instance, validated_data):
        user = self.context['request'].user

        orig_checkout_status = instance.fchkstatus
        new_checkout_status = validated_data['fchkstatus']
        new_checkout_chkoutfile = validated_data['fchkoutfile']

        if orig_checkout_status == "1-ASK":
            if new_checkout_status == '3-Check In':
                raise serializers.ValidationError("未迁出不可进行迁入操作")

            elif new_checkout_status == '2-Check Out':

                if new_checkout_chkoutfile is None:
                    raise serializers.ValidationError("PBL名称为必输项")
                instance.fchkstatus = new_checkout_status
                instance.fchkoutfile = new_checkout_chkoutfile
                instance.fchkoutperson = user.name
                instance.fchkoutdte = datetime.datetime.now().strftime('%Y-%m-%d')
                instance.save()

            elif new_checkout_status == '4-Un Check Out':
                instance.fchkstatus = new_checkout_status
                instance.save()

        elif orig_checkout_status == '2-Check Out':
            if new_checkout_status == "1-ASK":
                raise serializers.ValidationError("该对象已经迁出，不可进行当前操作")

            elif new_checkout_status == '2-Check Out':
                instance.fchkoutfile = new_checkout_chkoutfile
                instance.save()

            elif new_checkout_status == '3-Check In':
                instance.fchkstatus = new_checkout_status
                instance.fchkinperson = user.name
                instance.fchkindte = datetime.datetime.now().strftime('%Y-%m-%d')
                instance.save()

            elif new_checkout_status == '4-Un Check Out':
                instance.fchkstatus = new_checkout_status
                instance.save()

        elif orig_checkout_status == '3-Check In':
            raise serializers.ValidationError("该对象已经迁入，不可再进行修改")

        elif orig_checkout_status == '4-Un Check Out':
            raise serializers.ValidationError("该状态下不可再进行修改")

        return instance
