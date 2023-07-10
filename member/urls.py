from django.urls import path

from member import views

urlpatterns = [
    path("other_members", views.MemberAPIView.as_view()),
    path('schedules/', views.ScheduleAPIView.as_view(), name='schedule-list'),
    path('schedules/<int:pk>/', views.ScheduleDetailAPIView.as_view(), name='schedule-detail'),
]