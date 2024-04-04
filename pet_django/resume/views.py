from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from resume.models import Industry
from resume.models import Position
from resume.serializers import IndustrySerializer


class IndustriesList(APIView):
    @staticmethod
    def get(request):
        # Уточнить есть ли какая-то валидация, что name точно есть
        name = request.query_params["name"]

        try:
            Position.objects.get(name=name)
        except Position.DoesNotExist:
            return Response(
                data={"message": "Position not found"}, status=status.HTTP_404_NOT_FOUND
            )

        industries = Industry.objects.all()
        serializer = IndustrySerializer(industries, many=True)

        return Response(serializer.data)


class CompetenciesList(APIView):
    @staticmethod
    def get(request):
        pass
