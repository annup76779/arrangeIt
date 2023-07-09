from rest_framework import serializers

from user.models import OrganizationUser, MemberUser, OrgJoinCodes, User, generate_unique_key, Role


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
        return member

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)

        join_code = self.context.get('join_code')
        if join_code:
            try:
                join_obj = OrgJoinCodes.objects.get(join_code=join_code)
            except OrgJoinCodes.DoesNotExist:
                return instance
            instance.member = join_obj.user
        return instance