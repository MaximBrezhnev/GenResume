from rest_framework import serializers
from resume.models import General
from resume.models import Industry
from resume.models import Leader
from resume.models import Position
from resume.models import Profession


class IndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Industry
        fields = ("industry_name",)


class PositionAndIndustriesListSerializer(serializers.ModelSerializer):
    industries = serializers.ListField(child=IndustrySerializer())

    class Meta:
        model = Position
        fields = (
            "position_name",
            "industries",
        )


class LeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leader
        fields = ("leader_experience",)


class GeneralSerializer(serializers.ModelSerializer):
    class Meta:
        model = General
        fields = ("general_experience",)


class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = ("professional_experience",)


class PositionIndustryAndCompetenciesSerializer(serializers.Serializer):
    industry_name = IndustrySerializer()
    leader_competencies = serializers.ListField(
        child=LeaderSerializer(), required=False
    )
    general_competencies = serializers.ListField(child=GeneralSerializer())
    professional_competencies = serializers.ListField(child=ProfessionSerializer())

    class Meta:
        model = Position
        fields = ("position_name",)
