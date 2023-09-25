from django.urls import path
from . import views
app_name = "movies_app"

urlpatterns = [
    path("", views.index, name='index'),
]