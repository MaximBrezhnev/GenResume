from smtplib import SMTPDataError
from smtplib import SMTPRecipientsRefused

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import OpenApiExample
from drf_spectacular.utils import OpenApiParameter
from drf_spectacular.utils import OpenApiResponse
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


@extend_schema(
    parameters=[
        OpenApiParameter(
            name="document_id",
            required=False,
            description="UUID документа (необязательный)",
            type=str,
            location=OpenApiParameter.QUERY,
        ),
        OpenApiParameter(
            name="position",
            required=True,
            description="Позиция (обязательный)",
            type=str,
            location=OpenApiParameter.QUERY,
        ),
    ],
    responses={200: ShowIndustriesSerializer, 404: ShowPositionTypesSerializer},
)
@api_view(["GET"])
def check_position(request: Request) -> Response:
    """View, возвращающее полученную позицию и список отраслей для
    последующего выбора, если такая позиция уже существует. В противном
    случае возвращает полученную позицию и список типов позиций для
    последующего выбора. Если пользователь уже имеет документ с резюме,
    его uuid также вернется вместе с ответом"""

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


@extend_schema(
    request=CreatePositionSerializer,
    responses={
        200: ShowIndustriesSerializer,
        400: OpenApiResponse(response=None, description="Invalid data"),
    },
)
@api_view(["POST"])
def create_position(request: Request) -> Response:
    """View, создающее переданную позицию с указанным типом и возвращающее
    список отраслей для их последующего выбора. Если пользователь уже имеет документ с резюме,
    его id также вернется вместе с ответом"""
    deserializer = CreatePositionSerializer(data=request.data)

    if not deserializer.is_valid():
        return Response(
            data={"message": "Invalid data"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    response_data = get_response_data_when_creating(data=deserializer.data)
    return Response(data=ShowIndustriesSerializer(response_data).data)


@extend_schema(
    parameters=[
        OpenApiParameter(
            name="document_id",
            required=False,
            description="UUID документа (необязательный)",
            type=str,
            location=OpenApiParameter.QUERY,
        ),
        OpenApiParameter(
            name="position",
            required=True,
            description="Позиция (обязательный)",
            type=str,
            location=OpenApiParameter.QUERY,
        ),
        OpenApiParameter(
            name="industry",
            required=True,
            description="Отрасль (обязательный)",
            type=str,
            location=OpenApiParameter.QUERY,
        ),
    ],
    responses={
        200: ShowSeveralCompetenciesSerializer,
        409: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            examples=[
                OpenApiExample(
                    "Conflict Example",
                    summary="Conflict: The position and industry are already in the document",
                    value={
                        "document_id": "example-uuid",
                        "message": "These position and industry are already in the document",
                    },
                )
            ],
            description="Conflict: The position and industry are already in the document, returns document ID and "
            "message",
        ),
    },
)
@api_view(["GET"])
def get_competencies(request: Request) -> Response:
    """View, возвращающее список компетенций, которые
    соответствуют полученной позиции и отрасли. В случае,
    если пользователь в рамках сессии уже имеет документ с резюме,
    компетенции из него также возвращаются"""

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


@extend_schema(
    request=GetResumeSerializer,
    responses={
        200: OpenApiResponse(response=None, description="E-mail was sent"),
        400: OpenApiResponse(response=None, description="Invalid data"),
        422: OpenApiResponse(response=None, description="Cannot send email"),
    },
)
@api_view(["POST"])
def get_resume(request: Request) -> Response:
    """View, отправляющее письмо, содержащее резюме,
    на полученный адрес электронной почты"""

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
