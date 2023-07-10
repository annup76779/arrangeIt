from rest_framework.response import Response
from rest_framework.views import APIView

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
