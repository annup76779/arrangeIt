from rest_framework.response import Response
from rest_framework.views import APIView

from organization.serializer import OrgRoleSerializer
from user.customer_permission import IsOrgAuthenticated


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
