from django.urls import path

from extended_app import views

urlpatterns = [
    path("", views.index)
]
