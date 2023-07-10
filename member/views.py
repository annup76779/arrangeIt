from datetime import datetime, timedelta
from pytz import timezone

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from member.models import Schedule
from member.serializer import ScheduleSerializer
from user.customer_permission import IsMemberAuthenticated
from user.models import MemberUser
from user.serializer import MemberSerializer

# Create your views here.


class MemberAPIView(APIView):
    permission_classes = [IsMemberAuthenticated]

    def get(self, request):
        page = request.GET.get('page', 0)
        # access all the member that belong the organization that the current member belongs to.
        members = MemberUser.objects.filter(is_active=True, is_staff=True, member=request.user.member)[page*10: page*10+10]
        count = MemberUser.objects.filter(is_active=True, member=request.user).count()
        srlz = MemberSerializer(members, many=True)
        return Response({"members": srlz.data, "current_page": page, "per_page": 10, "total_page": count})


class ScheduleAPIView(generics.ListCreateAPIView):
    permission_classes = [IsMemberAuthenticated]
    serializer_class = ScheduleSerializer

    def get_queryset(self):
        date = datetime.now(tz=timezone("Asia/Kolkata"))
        start = datetime(date.year, date.month, date.day, tzinfo=timezone("Asia/Kolkata"))
        end = start + timedelta(days=1)
        return Schedule.objects.filter(member=self.request.user, start__range=[start, end]).order_by("-start")

    def create(self, request, *args, **kwargs):
        data = dict(**request.data)
        data['start'] = datetime.strptime(data["start"], '%a %b %d %Y %H:%M:%S')
        data['end'] = datetime.strptime(data["end"], '%a %b %d %Y %H:%M:%S')
        data.update({"member": request.user.pk})
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ScheduleDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsMemberAuthenticated]
    serializer_class = ScheduleSerializer

    def get_queryset(self):
        date = datetime.now(tz=timezone("Asia/Kolkata"))
        start = datetime(date.year, date.month, date.day, tzinfo=timezone("Asia/Kolkata"))
        end = start + timedelta(days=1)
        return Schedule.objects.filter(member=self.request.user, start__range=[start, end]).order_by("-start")

