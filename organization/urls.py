from django.urls import path
from . import views

urlpatterns = [
    path("create_role", views.OrgRolesAPI.as_view())
]

