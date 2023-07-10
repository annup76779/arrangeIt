from pytz import timezone
from rest_framework import serializers

from member.models import Schedule
from user.models import Notice, OrganizationUser, MemberUser, OrgJoinCodes, User, generate_unique_key, Role, \
    Member_role_in_org


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberUser
        fields = ('id', 'first_name', 'email')
        #follow up code


class ScheduleSerializer(serializers.ModelSerializer):
    start = serializers.DateTimeField(format='%a %b %d %Y %H:%M:%S')
    end = serializers.DateTimeField(format='%a %b %d %Y %H:%M:%S')

    class Meta:
        model = Schedule
        fields = "__all__"

    def validate_start(self, value):
        tz = timezone('Asia/Kolkata')  # IST timezone
        value = value.astimezone(tz)
        return value

    def validate_end(self, value):
        tz = timezone('Asia/Kolkata')  # IST timezone
        value = value.astimezone(tz)
        return value


