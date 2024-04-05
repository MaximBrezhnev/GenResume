from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from resume.models import General
from resume.models import Industry
from resume.models import Leader
from resume.models import Position
from resume.models import Profession
from resume.serializers import PositionAndIndustriesListSerializer
from resume.serializers import PositionIndustryAndCompetenciesSerializer


class IndustriesList(APIView):
    def get(self, request):
        position_name = request.query_params["position_name"]

        try:
            position = Position.objects.get(position_name__iexact=position_name)
            industries = Industry.objects.all()
        except Position.DoesNotExist:
            return Response(
                data={"message": "Position not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = PositionAndIndustriesListSerializer(
            {
                "position_name": position.position_name,
                "industries": industries,
            }
        )
        return Response(serializer.data)


class CompetenciesList(APIView):
    def get(self, request):
        position_name = request.query_params["position_name"]
        industry_name = request.query_params["industry_name"]

        position_type = Position.objects.get(
            position_name__iexact=position_name
        ).position_type

        general_competencies = General.objects.filter(position_type=position_type)
        professional_competencies = Profession.objects.filter(
            position_type=position_type
        ).filter(industry=Industry.objects.get(industry_name__iexact=industry_name))

        data = {
            "position_name": position_name,
            "industry": Industry.objects.get(industry_name__iexact=industry_name),
            "general_competencies": general_competencies,
            "professional_competencies": professional_competencies,
        }

        if position_type.is_leader:
            leader_competencies = Leader.objects.filter(position_type=position_type)
            data.update({"leader_competencies": leader_competencies})

        serializer = PositionIndustryAndCompetenciesSerializer(data)
        return Response(serializer.data)
