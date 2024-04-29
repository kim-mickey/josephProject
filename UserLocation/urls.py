from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="search"),
    path("error/", views.error_view, name="error"),
]
