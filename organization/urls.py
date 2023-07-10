from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


urlpatterns = [
    path("create_role", views.OrgRolesAPI.as_view()),
    path("edit_role/<int:id_>", views.OrgRolesAPI.as_view()),
    path("delete_role/<int:id_>", views.OrgRolesAPI.as_view()),

    path("list_role", views.OrgRoleViewAPI.as_view()),

    path("join_requests", views.JoinRequestAPI.as_view()),  # GET
    path("process_join_request", views.JoinRequestAPI.as_view()),  # POST ["accept", "reject"]

    path("member_list", views.OrgMemberAPI.as_view()),
]

