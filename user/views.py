import threading
from datetime import timedelta
import smtplib
from email.mime.text import MIMEText

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

            # Send email to the registered user
            subject = "Registration Successful",
            recipients = org.email
            message = f"Thank you for joining our organization. Your join code is: {org.join_code.join_code}.Kindly, Do not share this code with anyone!"
            thread = threading.Thread(target=send_email, args=(recipients, subject, message))
            thread.start()

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
        # try:
            srlz = MemberSerializer(data=request.data, context={"join_code": request.data.get("join_code"),
                                                                "role_id": request.data.get("role_id")})
            if srlz.is_valid():
                member_obj = srlz.save()

                # Send email to the registered user
                subject = "Registration Successful",
                recipients = member_obj.email
                message = f"Thank you for joining our organization. Your join code is: {member_obj.member.join_code.join_code}.Kindly, Do not share this code with anyone!"
                thread = threading.Thread(target=send_email, args=(recipients, subject, message))
                thread.start()

                return Response({"msg": "Successfully joined organization - `%s` as member." % member_obj.member.first_name})
            else:
                return Response({"error": str(srlz.errors)}, status=500)
        # except Exception as error:
        #     return Response({"error": str(error)}, status=500)


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


def send_email(to_email, subject, message):
    # Configure Gmail SMTP server details
    smtp_host = "smtp.gmail.com"
    smtp_port = 587
    smtp_username = "annup76779@gmail.com"
    smtp_password = "naocvdqztvjdoudg"
    sender_email = "annup76779@gmail.com"

    # Create a MIME message
    msg = MIMEText(message)
    msg['Subject'] = subject[0]
    msg['From'] = sender_email
    msg['To'] = to_email

    # Send the email
    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(msg)
