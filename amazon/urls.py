from django.urls import path

from . import views

urlpatterns = [
    path("", views.add_image, name="index"),
    path("images/", views.images, name="images"),
]
