from django.db import models


class DisplayMixin:
    name = None

    def __repr__(self):
        return self.name


class Position(DisplayMixin, models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)
    position_type = models.ForeignKey(to="PositionType", on_delete=models.PROTECT)


class PositionType(DisplayMixin, models.Model):
    class IsLeader(models.IntegerChoices):
        YES = 1, "Да"
        NO = 0, "Нет"

    name = models.CharField(max_length=100, unique=True)
    is_leader = models.BooleanField(
        choices=map(lambda x: (bool(x[0]), bool(x[1])), IsLeader.choices)
    )


class Industry(DisplayMixin, models.Model):
    name = models.CharField(max_length=100, unique=True)


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
