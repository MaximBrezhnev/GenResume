from typing import Optional

from resume.services.db_services import create_new_position
from resume.services.db_services import get_general_competencies
from resume.services.db_services import get_industries
from resume.services.db_services import get_leader_competencies
from resume.services.db_services import get_position_name
from resume.services.db_services import get_position_type_by_position_name
from resume.services.db_services import get_position_types
from resume.services.db_services import get_professional_competencies
from resume.services.document_services import extend_document
from resume.services.document_services import generate_document
from resume.services.document_services import get_data_from_document
from resume.tasks import send_file_by_email


def get_position_and_industries(document_id: Optional[str], position: str) -> dict:
    data = _form_data_with_position_and_industries(
        position_name=get_position_name(position=position)
    )
    _add_document_id_to_data(document_id=document_id, data=data)
    return data


def _form_data_with_position_and_industries(position_name: str) -> dict:
    return {
        "position": position_name,
        "industries": get_industries(),
    }


def _add_document_id_to_data(document_id: Optional[str], data: dict) -> None:
    if document_id is not None:
        data.update({"document_id": document_id})


def get_position_and_types(document_id: Optional[str], position: str) -> dict:
    data = _form_data_with_position_and_types(position_name=position)
    _add_document_id_to_data(document_id=document_id, data=data)
    return data


def _form_data_with_position_and_types(position_name: str) -> dict:
    return {
        "position": position_name.capitalize(),
        "position_types": get_position_types(),
    }


def get_response_data_when_creating(data: dict) -> dict:
    new_position = create_new_position(
        position=data.get("position_name"), position_type=data.get("position_type")
    ).position_name

    data = _form_data_with_position_and_industries(position_name=new_position)
    _add_document_id_to_data(document_id=data.get("document_id", None), data=data)
    return data


def get_list_of_competencies(
    document_id: Optional[str], position: str, industry: str
) -> dict:
    data = _form_data_when_getting_competencies(position=position, industry=industry)
    return _format_data_when_getting_competencies(data=data, document_id=document_id)


def _form_data_when_getting_competencies(position: str, industry: str) -> dict:
    position_type = get_position_type_by_position_name(position=position)
    data = {
        "position": position,
        "industry": industry,
        "general_competencies": get_general_competencies(position_type=position_type),
        "professional_competencies": get_professional_competencies(
            position_type=position_type, industry=industry
        ),
    }

    if position_type.is_leader:
        data.update(
            {
                "leader_competencies": get_leader_competencies(
                    position_type=position_type
                )
            }
        )
    return data


def _format_data_when_getting_competencies(
    document_id: Optional[str], data: dict
) -> dict:
    if document_id is None:
        document_id = generate_document(data)
        return {
            "document_id": document_id,
            "positions": [data],
        }
    else:
        new_document_id = extend_document(document_id, data)
        data_from_document = get_data_from_document(document_id)
        data_from_document.append(data)
        return {
            "document_id": new_document_id,
            "positions": data_from_document,
        }


def send_resume(data: dict) -> None:
    # Возможно, в этом причина медленной работы, в рамках рефакторинг посмотреть
    send_file_by_email(**data)
