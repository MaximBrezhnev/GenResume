from django.urls import path
from resume import views

urlpatterns = [
    path("check-position/", views.check_position, name="check-position"),
    path("competencies/", views.get_competencies, name="list-of-competencies"),
    path("create-position/", views.create_position, name="create-position"),
    path("get-resume/", views.get_resume, name="get-resume"),
]
