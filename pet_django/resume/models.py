import re

from django.db import models


class DisplayMixin:
    def __str__(self):
        for attr in self.__dict__:
            if re.match(r".*_name", attr):
                return self.__getattribute__(attr)
            elif re.match(r".*_experience", attr):
                if len(self.__getattribute__(attr).split()) > 3:
                    return " ".join(self.__getattribute__(attr).split()[:3]) + "..."
                return " ".join(self.__getattribute__(attr).split()[:3])


class Position(DisplayMixin, models.Model):
    position_name = models.CharField(
        max_length=100, unique=True, db_index=True, verbose_name="Название"
    )
    position_type = models.ForeignKey(
        to="PositionType", on_delete=models.PROTECT, verbose_name="Тип"
    )

    class Meta:
        verbose_name = "Позиция"
        verbose_name_plural = "Позиции"


class PositionType(DisplayMixin, models.Model):
    class IsLeader(models.IntegerChoices):
        YES = 1, "Да"
        NO = 0, "Нет"

    position_type_name = models.CharField(
        max_length=100, unique=True, verbose_name="Название"
    )
    is_leader = models.BooleanField(
        choices=map(lambda x: (bool(x[0]), x[1]), IsLeader.choices),
        verbose_name="Лидер",
    )

    class Meta:
        verbose_name = "Тип позиции"
        verbose_name_plural = "Типы позиций"


class Industry(DisplayMixin, models.Model):
    industry_name = models.CharField(
        max_length=100, unique=True, verbose_name="Название"
    )

    class Meta:
        verbose_name = "Отрасль"
        verbose_name_plural = "Отрасли"


class Profession(DisplayMixin, models.Model):
    professional_experience = models.TextField(unique=True, verbose_name="Опыт")
    position_type = models.ForeignKey(
        to="PositionType", on_delete=models.PROTECT, verbose_name="Тип позиции"
    )
    industry = models.ForeignKey(
        to="Industry", on_delete=models.PROTECT, verbose_name="Отрасль"
    )

    class Meta:
        verbose_name = "Профессиональный опыт"
        verbose_name_plural = "Профессиональные компетенции"


class General(DisplayMixin, models.Model):
    general_experience = models.TextField(unique=True, verbose_name="Опыт")
    position_type = models.ForeignKey(
        to="PositionType", on_delete=models.PROTECT, verbose_name="Тип позиции"
    )

    class Meta:
        verbose_name = "Общий опыт"
        verbose_name_plural = "Общие компетенции"


class Leader(DisplayMixin, models.Model):
    leader_experience = models.TextField(unique=True, verbose_name="Опыт")
    position_type = models.ForeignKey(
        to="PositionType", on_delete=models.PROTECT, verbose_name="Тип позиции"
    )

    class Meta:
        verbose_name = "Опыт лидера"
        verbose_name_plural = "Лидерские компетенции"
