from django.db import transaction
from rest_framework import serializers

from systems.models import Systems


class SystemsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Systems
        fields = "__all__"

    @transaction.atomic()
    def create(self, validated_data):

        user = self.context['request'].user

        organization_id = user.ammic_organization.id
        if not user.ammic_organization.isgroup:
            organization_id = user.ammic_organization.parent.id

        new_fsystemcd = validated_data['fsystemcd']

        is_exist = Systems.objects.filter(fsystemcd__exact=new_fsystemcd, organization_id=organization_id)
        if is_exist.count() > 0:
            raise serializers.ValidationError("系统代码已经存在")

        systems = Systems.objects.create(**validated_data)

        systems.organization_id = organization_id

        systems.save()

        return systems
