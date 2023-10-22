from django.contrib.auth import views as auth_views
from django.urls import path

from accounts import views


app_name = "accounts"

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path("login/", views.LoginView.as_view(), name="login"),
    path(
        "logout",
        auth_views.LogoutView.as_view(next_page="accounts:login"),
        name="logout",
    ),
    path("edit/", views.EditAccountView.as_view(), name="edit"),
]
