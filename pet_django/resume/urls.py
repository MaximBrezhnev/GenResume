from django.urls import path
from resume import views

urlpatterns = [path("", views.IndustriesList.as_view(), name="list-of-industries")]
