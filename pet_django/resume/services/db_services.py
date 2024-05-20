from resume.models import General
from resume.models import Industry
from resume.models import Leader
from resume.models import Position
from resume.models import PositionType
from resume.models import Profession


def get_position_name(position: str) -> str:
    position = _format_position_name(position_name=position)
    return Position.objects.get(position_name__exact=position).position_name


def _format_position_name(position_name: str) -> str:
    return position_name.strip().capitalize()


def get_industries() -> list[Industry]:
    return [industry.industry_name for industry in Industry.objects.all()]


def get_position_types() -> list[PositionType]:
    return [p_type.position_type_name for p_type in PositionType.objects.all()]


def create_new_position(position: str, position_type: str) -> Position:
    position = _format_position_name(position_name=position)
    return Position.objects.create(
        position_name=position,
        position_type=_get_position_type(position_type=position_type),
    )


def _get_position_type(position_type: str) -> PositionType:
    return PositionType.objects.get(position_type_name=position_type)


def get_position_type_by_position_name(position: str) -> PositionType:
    return Position.objects.get(position_name=position).position_type


def get_general_competencies(position_type: PositionType) -> list[General]:
    return [
        competency.general_experience
        for competency in General.objects.filter(position_type=position_type)
    ]


def get_professional_competencies(
    position_type: PositionType, industry: str
) -> list[Profession]:
    return [
        competency.professional_experience
        for competency in Profession.objects.filter(
            position_type=position_type,
            industry__industry_name=industry,
        )
    ]


def get_leader_competencies(position_type: PositionType) -> list[Leader]:
    return [
        competency.leader_experience
        for competency in Leader.objects.filter(position_type=position_type)
    ]
