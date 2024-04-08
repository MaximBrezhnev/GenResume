from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from resume.actions import generate_document
from resume.actions import get_data_from_document
from resume.models import General
from resume.models import Industry
from resume.models import Leader
from resume.models import Position
from resume.models import PositionType
from resume.models import Profession
from resume.serializers import CreatePositionSerializer
from resume.serializers import ShowCompetenciesSerializer
from resume.serializers import ShowIndustriesSerializer
from resume.serializers import ShowPositionTypesSerializer


@api_view(["GET"])
def check_position(request):
    position_name = request.query_params["position_name"]
    document_id = request.query_params.get("document_id", None)

    data = {}
    if document_id is not None:
        data["document_id"] = document_id

    try:
        position = Position.objects.get(position_name__iexact=position_name)
        industries = [obj.industry_name for obj in Industry.objects.all()]
        data.update(
            {
                "position_name": position.position_name,
                "industries": industries,
            }
        )

        serializer = ShowIndustriesSerializer(data)
        return Response(
            data=serializer.data,
        )

    except Position.DoesNotExist:
        position_types = [obj.position_type_name for obj in PositionType.objects.all()]
        data.update({"position_types": position_types})

        serializer = ShowPositionTypesSerializer(data)
        return Response(
            data=serializer.data,
            status=status.HTTP_404_NOT_FOUND,
        )


@api_view(["POST"])
def create_position(request):
    serializer_for_request = CreatePositionSerializer(data=request.data)

    if not serializer_for_request.is_valid():
        return Response(
            data={"message": "Invalid data"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    data_from_request = serializer_for_request.data

    data_for_response = {}
    if serializer_for_request.data.get("document_id", None) is not None:
        data_for_response.update({"document_id": data_from_request["document_id"]})

    position_type = PositionType.objects.get(
        position_type_name=data_from_request["position_type_name"]
    )
    new_position = Position.objects.create(
        position_name=data_from_request["position_name"].capitalize(),
        position_type=position_type,
    )
    industries = [obj.industry_name for obj in Industry.objects.all()]

    data_for_response.update(
        {
            "position_name": new_position.position_name,
            "industries": industries,
        }
    )

    serializer_for_response = ShowIndustriesSerializer(data_for_response)
    return Response(data=serializer_for_response.data)


# @api_view(["GET"])
# def get_competencies(request):
#     position_name = request.query_params["position_name"]
#     industry_name = request.query_params["industry_name"]
#     position_type = Position.objects.get(
#         position_name=position_name
#     ).position_type
#
#     general_competencies = [
#         obj.general_experience for obj in General.objects.filter(position_type=position_type)
#     ]
#     professional_competencies = [
#         obj.professional_experience for obj in
#         Profession.objects.filter(
#             position_type=position_type,
#             industry=Industry.objects.get(industry_name=industry_name))
#     ]
#     data = {
#         "position_name": position_name,
#         "industry": industry_name,
#         "general_competencies": general_competencies,
#         "professional_competencies": professional_competencies,
#     }
#     if position_type.is_leader:
#         leader_competencies = [
#             obj.leader_experience for obj in
#             Leader.objects.filter(position_type=position_type)
#         ]
#         data.update({"leader_competencies": leader_competencies})
#
#     # Провести рефакторинг условного оператора
#     document_id = request.query_params.get("document_id", None)
#     if document_id is None:
#         document_id = generate_document(data)
#         data.update({"document_id": document_id})
#         serializer = ShowCompetenciesSerializer(data)
#         return Response(serializer.data)
#
#     data.update(get_data_from_document(document_id))
#     print(data)
#     return Response()


@api_view(["GET"])
def get_competencies(request):
    position_name = request.query_params["position_name"]
    industry_name = request.query_params["industry_name"]
    document_id = request.get("document_id", None)
    position_type = Position.objects.get(position_name=position_name).position_type

    general_competencies = [
        obj.general_experience
        for obj in General.objects.filter(position_type=position_type)
    ]
    professional_competencies = [
        obj.professional_experience
        for obj in Profession.objects.filter(
            position_type=position_type,
            industry=Industry.objects.get(industry_name=industry_name),
        )
    ]
    data = {
        "position_name": position_name,
        "industry": industry_name,
        "general_competencies": general_competencies,
        "professional_competencies": professional_competencies,
    }
    if position_type.is_leader:
        leader_competencies = [
            obj.leader_experience
            for obj in Leader.objects.filter(position_type=position_type)
        ]
        data.update({"leader_competencies": leader_competencies})

    if document_id is None:
        document_id = generate_document(data)
        data.update({"document_id": document_id})
        serializer = ShowCompetenciesSerializer(data)
        return Response(serializer.data)

    data.update(get_data_from_document(document_id))
    print(data)
    return Response()


@api_view(["GET"])
def get_resume(request):
    pass
