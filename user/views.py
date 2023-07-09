from rest_framework.response import Response
from rest_framework.views import APIView

from .serializer import *


# Create your views here.
class OrganizerRegisterView(APIView):
    def post(self, request):
        srlz = OrgSerializer(data={
            "email": request.data.get("email"),
            "password": request.data.get("password")
        },
        context={"first_name": request.data.get("org_name")})
        if srlz.is_valid():
            org = srlz.save()
            return Response({'msg': "New organization registered.", "join_code": org.join_code.join_code})
        else:
            return Response({"error": str(srlz.errors)}, status=500)


class ManagerRegisterView(APIView):
    def post(self, request):
        try:
            srlz = MemberSerializer(data=request.data, context={"join_code": request.data.get("join_code")})
            if srlz.is_valid():
                member_obj = srlz.save()
                return Response({"msg": "Successfully joined organization - `%s` as member." % member_obj.member.first_name})
            else:
                return Response({"error": str(srlz.errors)}, status=500)
        except Exception as error:
            return Response({"error": str(error)}, status=500)

