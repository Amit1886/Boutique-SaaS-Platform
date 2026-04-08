from django.urls import path

from . import views

urlpatterns = [
    path("github/", views.github_deploy_hook, name="github_deploy_hook"),
]

