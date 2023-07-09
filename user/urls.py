from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("login", views.LoginAPI.as_view(), name='login'),

    path("org/register", views.OrganizerRegisterView.as_view()),
    path("member/register", views.ManagerRegisterView.as_view()),
]



