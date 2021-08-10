from django.db import transaction
from rest_framework import serializers

from reviews.models import CodeReview


class DesignReviewSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = CodeReview
        fields = ('id', 'fslipno', 'fobjectid', 'fcontent_text')

    @transaction.atomic()
    def create(self, validated_data):
        user = self.context['request'].user
        design = CodeReview.objects.create(**validated_data)
        design.fobjectid = "Design Review"
        design.fentusr = user.name
        design.fupdteprg = 'Design Review New'
        design.save()
        return design


class CodeReviewSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = CodeReview
        fields = ('id', 'fslipno', 'fobjectid', 'fcontent_text')

    @transaction.atomic()
    def create(self, validated_data):
        user = self.context['request'].user
        code = CodeReview.objects.create(**validated_data)
        code.fentusr = user.name
        code.fupdteprg = 'Code Review New'
        code.save()
        return code
