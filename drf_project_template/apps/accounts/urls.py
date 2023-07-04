from django.urls import path, re_path
from drf_project_template.apps.accounts import views

urlpatterns = [
    path("register/", views.RegistrationView.as_view(), name="register"),
]