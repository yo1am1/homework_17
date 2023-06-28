from django.urls import path

from . import views

urlpatterns = [
    path("", views.add_image, name="index"),
    path("images/", views.images, name="images"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("callback", views.callback, name="callback"),
]
