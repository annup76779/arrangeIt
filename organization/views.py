from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from organization.serializer import OrgRoleSerializer
from user.customer_permission import IsOrgAuthenticated
from user.models import MemberUser, Role
from user.serializer import MemberSerializer
from rest_framework.pagination import PageNumberPagination


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
    serializer_class = OrgRoleSerializer

    def get_queryset(self):
        user = self.request.user
        return Role.objects.filter(organization=user)


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
    

class MemberListAPI(generics.ListAPIView):
    serializer_class = MemberSerializer
    queryset = MemberUser.objects.all()
    pagination_class = CustomPagination