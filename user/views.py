from datetime import timedelta

from rest_framework.response import Response
from rest_framework.views import APIView

from .helper import get_tokens_for_user
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


class LoginAPI(APIView):
    def post(self, request):
        try:
            email = request.data.get('email')
            password = request.data.get('password')
            try:
                user = User.objects.get(email=email, role__in=[1, 2])
                if user.check_password(password):
                    tokens = get_tokens_for_user(user)
                    return Response(tokens)
                else:
                    return Response({"msg": "Wrong password"})
            except User.DoesNotExist:
                return Response({"msg": "No user member or organization."})
        except Exception as error:
            return Response({"error": str(error)}, status=500)


class ManagerRegisterView(APIView):
    def post(self, request):
        try:
            srlz = MemberSerializer(data=request.data, context={"join_code": request.data.get("join_code"),
                                                                "role_id": request.data.get("role_id")})
            if srlz.is_valid():
                member_obj = srlz.save()
                return Response({"msg": "Successfully joined organization - `%s` as member." % member_obj.member.first_name})
            else:
                return Response({"error": str(srlz.errors)}, status=500)
        except Exception as error:
            return Response({"error": str(error)}, status=500)


class RolesOfOrgByCode(APIView):
    def get(self, request, join_code):
        try:
            org = OrgJoinCodes.objects.get(join_code=join_code)
            roles = [
                {'id': role.id, 'name': role.name}
                for role in org.user.created_role.all()
            ]
            return Response({"roles": roles})
        except Exception as error:
            return Response({"error": str(error)}, status=500)

