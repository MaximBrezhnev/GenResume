from smtplib import SMTPDataError
from smtplib import SMTPRecipientsRefused

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from resume.models import Position
from resume.serializers import CreatePositionSerializer
from resume.serializers import GetResumeSerializer
from resume.serializers import ShowIndustriesSerializer
from resume.serializers import ShowPositionTypesSerializer
from resume.serializers import ShowSeveralCompetenciesSerializer
from resume.services.services import get_list_of_competencies
from resume.services.services import get_position_and_industries
from resume.services.services import get_position_and_types
from resume.services.services import get_response_data_when_creating
from resume.services.services import send_resume


@api_view(["GET"])
def check_position(request: Request) -> Response:
    document_id = request.query_params.get("document_id", None)
    position = request.query_params.get("position")

    try:
        data = get_position_and_industries(document_id=document_id, position=position)
        return Response(
            data=ShowIndustriesSerializer(data).data,
        )

    except Position.DoesNotExist:
        data = get_position_and_types(document_id=document_id, position=position)
        return Response(
            data=ShowPositionTypesSerializer(data).data,
            status=status.HTTP_404_NOT_FOUND,
        )


@api_view(["POST"])
def create_position(request: Request) -> Response:
    deserializer = CreatePositionSerializer(data=request.data)

    if not deserializer.is_valid():
        return Response(
            data={"message": "Invalid data"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    response_data = get_response_data_when_creating(data=deserializer.data)
    return Response(data=ShowIndustriesSerializer(response_data).data)


@api_view(["GET"])
def get_competencies(request: Request) -> Response:
    position = request.query_params.get("position")
    industry = request.query_params.get("industry")
    document_id = request.query_params.get("document_id", None)

    try:
        data = get_list_of_competencies(
            position=position, industry=industry, document_id=document_id
        )
        return Response(data=ShowSeveralCompetenciesSerializer(data).data)
    except ValidationError:
        return Response(
            data={
                "document_id": document_id,
                "message": "These position and industry are already in the document",
            },
            status=status.HTTP_409_CONFLICT,
        )


@api_view(["POST"])
def get_resume(request: Request) -> Response:
    deserializer = GetResumeSerializer(data=request.data)

    if not deserializer.is_valid():
        return Response(
            data={"message": "Invalid data"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        send_resume(data=deserializer.data)
        return Response(data={"message": "The e-mail was sent"})
    except (SMTPRecipientsRefused, SMTPDataError):
        return Response(
            data={"message": "Cannot send email"},
            status=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
