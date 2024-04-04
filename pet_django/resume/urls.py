from django.urls import path
from resume import views

urlpatterns = [
    path("industries/", views.IndustriesList.as_view(), name="list-of-industries"),
    path(
        "competencies/", views.CompetenciesList.as_view(), name="list-of-competencies"
    ),
]
