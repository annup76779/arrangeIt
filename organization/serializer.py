from rest_framework import serializers

from user.models import OrganizationUser, MemberUser, OrgJoinCodes, User, generate_unique_key, Role


class OrgRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ('name', 'add_time_table', 'update_status')

    def create(self, validated_data):
        return self.Meta.model.objects.create(**validated_data, organization=self.context.pop("user"))

