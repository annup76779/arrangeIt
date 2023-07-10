from datetime import timedelta, datetime

from pytz import timezone
from rest_framework import serializers

from user.models import Notice, OrganizationUser, MemberUser, OrgJoinCodes, User, generate_unique_key, Role, \
    Member_role_in_org


class OrgSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationUser
        fields = ("email", "password",)

    def create(self, validated_data):
        obj = self.Meta.model.objects.create_user(**validated_data, first_name=self.context.get("first_name"))
        # if the new user is not an organization
        if obj.role != User.Role.ORG:
            return obj
        # generating the join code when the new organization user is registered
        join_code = generate_unique_key()
        join_obj = OrgJoinCodes.objects.filter(join_code=join_code).first()
        count = 7
        while join_obj:
            join_code = generate_unique_key(count)
            count += 1
            join_obj = OrgJoinCodes.objects.filter(join_code=join_code).first()

        OrgJoinCodes.objects.create(join_code=join_code, user=obj)
        return obj


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberUser
        fields = ("email", "password", "first_name")

    def create(self, validated_data):
        join_code = self.context.pop("join_code")
        member = self.Meta.model.objects.create_user(**validated_data, join_code=join_code)
        try:
            org_role = Role.objects.get(id=self.context.get("role_id"))
            Member_role_in_org.objects.create(member=member, role=org_role)
        except Exception as error:
            member.delete()
            raise Exception(str(error))
        return member

    def to_representation(self, instance):
        date = datetime.now(tz=timezone("Asia/Kolkata"))
        start = datetime(date.year, date.month, date.day, tzinfo=timezone("Asia/Kolkata"))
        end = start + timedelta(days=1)
        schedule = instance.schedule.filter(start__in=[start, end]).all()
        if schedule:
            status = True
        else:
            status = False

        output = {
            "id": instance.id,
            "name": instance.first_name,
            "email": instance.email,
            "role_in_org": instance.role_in_org.role.name.title(),
            "status": status
        }
        return output


class MemberProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberUser
        fields = ("email", "first_name")

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['role'] = instance.role_in_org.role.name.title()
        return data

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)

        join_code = self.context.get('join_code')
        if join_code:
            try:
                join_obj = OrgJoinCodes.objects.get(join_code=join_code)
            except OrgJoinCodes.DoesNotExist:
                return instance
            instance.member = join_obj.user

        if self.context.get("role_id"):
            old_role = instance.role_in_org.role
            try:
                instance.role_in_org.delete()
                new_role = Role.objects.get(id=self.context.get("role_id"))
                Member_role_in_org.objects.create(member=instance, role=new_role)
            except Role.DoesNotExist:
                self.context["error_message"] = "Role requested is not registered with the org."
                Member_role_in_org.objects.create(member=instance, role=old_role)
            except Exception as error:
                self.context["error_message"] = str(error)
                Member_role_in_org.objects.create(member=instance, role=old_role)
        return instance


class JoinCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrgJoinCodes
        fields = ["join_code", ]


class OrgProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrganizationUser
        fields = ("email", "first_name", "role")
        read_only_fields = ["role"]

    def to_representation(self, instance):
        output = super().to_representation(instance)
        output.update({"join_code": instance.join_code.join_code})
        return output


class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = ('id', 'title', 'content', 'published_at')
        read_only_fields = ('id', 'published_at')

