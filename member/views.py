from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from organization.serializer import OrgRoleSerializer
from user.customer_permission import IsMemberAuthenticated, IsOrgAuthenticated
from user.models import MemberUser, Notice, Role
from user.serializer import MemberSerializer, NoticeSerializer

# Create your views here.

class OrgMemberAPI(APIView):
    permission_classes = [IsMemberAuthenticated]

    def get(self, request):
        page = request.GET.get('page', 0)
        members = MemberUser.objects.filter(is_active=True, is_staff=True, member=request.user)[page*10: page*10+10]
        count = MemberUser.objects.filter(is_active=True, member=request.user).count()
        srlz = MemberSerializer(members, many=True)
        return Response({"members": srlz.data, "current_page": page, "per_page": 10, "total_page": count})

    def delete(self, request, id):
        try:
            member = MemberUser.objects.get(id=id)
            member.delete()
            return Response({"msg": "Deleted"})
        except MemberUser.DoesNotExist:
            return Response({"error": "No such member"})