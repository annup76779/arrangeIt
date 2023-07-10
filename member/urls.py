from django.urls import path

from member import views

urlpatterns = [
    path("other_members", views.MemberAPIView.as_view())
]