from django.contrib import admin
from django.db.models import Field
from django.http import HttpRequest

from .models import General
from .models import Industry
from .models import Leader
from .models import Position
from .models import PositionType
from .models import Profession


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = (
        "position_name",
        "position_type",
    )
    search_fields = ("position_name",)


@admin.register(PositionType)
class PositionTypeAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = (
        "position_type_name",
        "is_leader",
    )


@admin.register(Industry)
class IndustryAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ("industry_name",)


MAX_NUMBER_OF_WORDS = 5


@admin.register(Profession)
class ProfessionAdmin(admin.ModelAdmin):
    list_per_page = 5
    list_display = (
        "shortened_professional_experience",
        "position_type",
        "industry",
    )

    def shortened_professional_experience(self, obj: Profession) -> str:
        if len(obj.professional_experience.split()) > MAX_NUMBER_OF_WORDS:
            return (
                " ".join(obj.professional_experience.split()[:MAX_NUMBER_OF_WORDS])
                + "..."
            )
        return " ".join(obj.professional_experience.split()[:MAX_NUMBER_OF_WORDS])

    shortened_professional_experience.short_description = "Опыт"


@admin.register(General)
class GeneralAdmin(admin.ModelAdmin):
    list_per_page = 5
    list_display = (
        "shortened_general_experience",
        "position_type",
    )

    def shortened_general_experience(self, obj: General) -> str:
        if len(obj.general_experience.split()) > MAX_NUMBER_OF_WORDS:
            return (
                " ".join(obj.general_experience.split()[:MAX_NUMBER_OF_WORDS]) + "..."
            )
        return " ".join(obj.general_experience.split()[:MAX_NUMBER_OF_WORDS])

    shortened_general_experience.short_description = "Опыт"


@admin.register(Leader)
class LeaderAdmin(admin.ModelAdmin):
    list_per_page = 5
    list_display = (
        "shortened_leader_experience",
        "position_type",
    )

    def shortened_leader_experience(self, obj: Leader) -> str:
        if len(obj.leader_experience.split()) > MAX_NUMBER_OF_WORDS:
            return " ".join(obj.leader_experience.split()[:MAX_NUMBER_OF_WORDS]) + "..."
        return " ".join(obj.leader_experience.split()[:MAX_NUMBER_OF_WORDS])

    shortened_leader_experience.short_description = "Опыт"

    def formfield_for_foreignkey(self, db_field: Field, request: HttpRequest, **kwargs):
        if db_field.name == "position_type":
            kwargs["queryset"] = PositionType.objects.filter(is_leader=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
