from django.db import transaction
from rest_framework import serializers

from projects.models import Projects


class ProjectsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Projects
        fields = "__all__"

    @transaction.atomic()
    def create(self, validated_data):

        user = self.context['request'].user

        organization_id = user.ammic_organization.id
        if not user.ammic_organization.isgroup:
            organization_id = user.ammic_organization.parent.id

        new_fprojectcd = validated_data['fprojectcd']

        is_exist = Projects.objects.filter(fprojectcd__exact=new_fprojectcd, organization_id=organization_id)
        if is_exist.count() > 0:
            raise serializers.ValidationError("制番号已经存在")

        projects = Projects.objects.create(**validated_data)

        projects.organization_id = organization_id

        projects.save()

        return projects
