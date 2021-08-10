from rest_framework import serializers

from liaisons.models import Liaisons
from qa.models import QaHead
from qa.serializers import QaHeadDisplayNoteSerializer


class ReportLiaisonSerializer(serializers.ModelSerializer):
    note = serializers.SerializerMethodField()

    class Meta:
        model = Liaisons
        fields = ('fsystemcd', 'fprojectcd', 'fodrno', 'note')

    def get_note(self, obj):
        all_qahf = QaHead.objects.filter(fslipno__exact=obj['fodrno'])
        qahf_serializer = QaHeadDisplayNoteSerializer(all_qahf, many=True, context={'request': self.context['request']})
        return qahf_serializer.data[0]['fnote'] if qahf_serializer.data else '******'


class ReportLiaisonListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Liaisons
        fields = ('fodrno', 'fsystemcd', 'fslipno', 'fsirno', 'fbrief')


class QaHeadPCLListSerializer(serializers.ModelSerializer):
    fodrno = serializers.SerializerMethodField()
    fsirno = serializers.SerializerMethodField()
    fbrief = serializers.SerializerMethodField()
    fsystemcd = serializers.SerializerMethodField()

    class Meta:
        model = QaHead
        fields = ('fodrno', 'fslipno', 'fsirno', 'fsystemcd', 'fbrief')

    def get_fodrno(self, obj):
        return obj.fslipno

    def get_fsirno(self, obj):
        return obj.fslipno2

    def get_fbrief(self, obj):
        return obj.fnote

    def get_fsystemcd(self, obj):
        return obj.ftesttyp
