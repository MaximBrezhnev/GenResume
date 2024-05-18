from django.urls import path
from resume import views

urlpatterns = [
    path("check-position/", views.check_position, name="check_position"),
    path("competencies/", views.get_competencies, name="list_of_competencies"),
    path("create-position/", views.create_position, name="create_position"),
    path("get-resume/", views.get_resume, name="get_resume"),
]
