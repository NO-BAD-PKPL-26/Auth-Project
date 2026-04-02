from django.urls import path
from .views import home_view, update_preferences_view

urlpatterns = [
    path("", home_view, name="home"),
    path("preferences/update/", update_preferences_view, name="update_preferences"),
]