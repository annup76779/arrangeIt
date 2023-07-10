from rest_framework import serializers

from user.models import Notice, OrganizationUser, MemberUser, OrgJoinCodes, User, generate_unique_key, Role, \
    Member_role_in_org


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberUser
        fields = ('id', 'first_name', 'email')
        #follow up code