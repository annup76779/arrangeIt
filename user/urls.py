from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path("org/register", views.OrganizerRegisterView.as_view()),
    # path("member", views.MemberLoginView.as_view()),
]



