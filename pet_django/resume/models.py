import re

from django.db import models


class DisplayMixin:
    def __str__(self):
        for attr in self.__dict__:
            if re.match(r".*_name", attr):
                return self.__getattribute__(attr)


class Position(DisplayMixin, models.Model):
    position_name = models.CharField(max_length=100, unique=True, db_index=True)
    position_type = models.ForeignKey(to="PositionType", on_delete=models.PROTECT)


class PositionType(DisplayMixin, models.Model):
    class IsLeader(models.IntegerChoices):
        YES = 1, "Да"
        NO = 0, "Нет"

    position_type_name = models.CharField(max_length=100, unique=True)
    is_leader = models.BooleanField(
        choices=map(lambda x: (bool(x[0]), bool(x[1])), IsLeader.choices)
    )


class Industry(DisplayMixin, models.Model):
    industry_name = models.CharField(max_length=100, unique=True)


class Profession(models.Model):
    professional_experience = models.TextField(unique=True)
    position_type = models.ForeignKey(to="PositionType", on_delete=models.PROTECT)
    industry = models.ForeignKey(to="Industry", on_delete=models.PROTECT)


class General(models.Model):
    general_experience = models.TextField(unique=True)
    position_type = models.ForeignKey(to="PositionType", on_delete=models.PROTECT)


class Leader(models.Model):
    leader_experience = models.TextField(unique=True)
    position_type = models.ForeignKey(to="PositionType", on_delete=models.PROTECT)


class Document(models.Model):
    def __str__(self):
        return self.filename

    filename = models.CharField(max_length=100, unique=True)
    file = models.FileField(upload_to="resume/documents")
