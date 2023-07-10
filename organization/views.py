from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from organization.serializer import OrgRoleSerializer
from user.customer_permission import IsOrgAuthenticated
from user.models import MemberUser, Notice, Role
from user.serializer import MemberSerializer, NoticeSerializer


class OrgRolesAPI(APIView):
    permission_classes = [IsOrgAuthenticated]

    def post(self, request):
        try:
            srlz = OrgRoleSerializer(data=request.data, context={"user": request.user})
            if srlz.is_valid():
                srlz.save()
                return Response({"msg": "New role created!"})
            else:
                return Response({"error": str(srlz.error)}, status=500)
        except Exception as error:
            return Response({"error": error.__str__()}, status=500)

    def put(self, request, id_):
        try:
            role = Role.objects.get(id=id_)
            srlz = OrgRoleSerializer(instance=role, data=request.data, context={"user": request.user})
            if srlz.is_valid():
                srlz.save()
                return Response({"msg": "Role `%s` updated!" % role.id})
            else:
                return Response({"error": str(srlz.error)}, status=500)
        except Role.DoesNotExist:
            return Response({"error": "Role does not exist"}, status=500)
        except Exception as error:
            return Response({"error": error.__str__()}, status=500)

    def delete(self, request, id_):
        try:
            role = Role.objects.get(id=id_)
            role.delete()
            return Response({"msg": "Role %s deleted" % id_})
        except Role.DoesNotExist:
            return Response({"error": "Role does not exist"}, status=500)
        except Exception as error:
            return Response({"error": error.__str__}, status=500)


class OrgRoleViewAPI(generics.ListAPIView):
    permission_classes = [IsOrgAuthenticated]
    serializer_class = OrgRoleSerializer

    def get_queryset(self):
        user = self.request.user
        return Role.objects.filter(organization=user)


class JoinRequestAPI(APIView):
    permission_classes = [IsOrgAuthenticated]
    def get(self, request):
        page = request.GET.get('page', 0)
        members = MemberUser.objects.filter(is_active=False, member=request.user).all()[page*10: page*10+10]
        count = MemberUser.objects.filter(is_active=False, member=request.user).count()
        srlz = MemberSerializer(members, many=True)
        return Response({"members": srlz.data, "current_page": page, "per_page": 10, "total_page": count})

    def post(self, request):
        try:
            members_ids = request.data.get("members")
            process_type = request.data.get("process_type", "reject")
            if process_type == "accept":
                process_type = True
            else:
                process_type = False
            issues = []
            for member_id in members_ids:
                try:
                    member = MemberUser.objects.get(id=member_id)
                    if not process_type:
                        member.delete()
                    else:
                        member.is_active = process_type
                        member.is_staff = process_type
                        member.save()
                except MemberUser.DoesNotExist:
                    issues.append({
                        "member_id": member_id,
                        "error": "Member does not exist"
                    })
            return Response({"msg": "Processed members!", "issues": issues})
        except Exception as error:
            return Response({"error": str(error)}, status=500)


class OrgMemberAPI(APIView):
    permission_classes = [IsOrgAuthenticated]
    def get(self, request):
        page = request.GET.get('page', 0)
        members = MemberUser.objects.filter(is_active=True, is_staff=True, member=request.user)[page*10: page*10+10]
        count = MemberUser.objects.filter(is_active=True, member=request.user).count()
        srlz = MemberSerializer(members, many=True)
        return Response({"members": srlz.data, "current_page": page, "per_page": 10, "total_page": count})


class NoticeListAPI(generics.ListCreateAPIView):
    serializer_class = NoticeSerializer
    permission_classes = [IsOrgAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Notice.objects.filter(organization=user.organization)

    def perform_create(self, serializer):
        serializer.save(organization=self.request.user.organization)


class NoticeDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NoticeSerializer
    permission_classes = [IsOrgAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Notice.objects.filter(organization=user.organization)