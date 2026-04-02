"""URL configuration for accounting app (web dashboard)."""

from django.urls import path

from . import views

app_name = "accounting"

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("", views.dashboard, name="dashboard"),
]
