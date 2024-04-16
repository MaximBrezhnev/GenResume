import string

from rest_framework import serializers
from resume.models import Position


class ShowPositionTypesSerializer(serializers.Serializer):
    document_id = serializers.UUIDField(required=False)
    position_name = serializers.CharField()
    position_types = serializers.ListField(child=serializers.CharField())


class ShowIndustriesSerializer(serializers.Serializer):
    document_id = serializers.UUIDField(required=False)
    position_name = serializers.CharField()
    industries = serializers.ListField(child=serializers.CharField())


class CompetenciesSerializer(serializers.Serializer):
    position_name = serializers.CharField()
    industry = serializers.CharField()
    leader_competencies = serializers.ListField(
        child=serializers.CharField(), required=False
    )
    general_competencies = serializers.ListSerializer(child=serializers.CharField())
    professional_competencies = serializers.ListSerializer(
        child=serializers.CharField()
    )


class ShowSeveralCompetenciesSerializer(serializers.Serializer):
    document_id = serializers.UUIDField()
    positions = serializers.ListSerializer(child=CompetenciesSerializer())


class CreatePositionSerializer(serializers.ModelSerializer):
    SYMBOLS = (
        string.ascii_letters
        + "йцукенгшщзхъфывапролджэячсмитьбюё"
        + "ЙЦУКЕНГШЩЗХФЫВАПРОЛДЖЭЯЧСМИТБЮЁ"
        + "-, "
    )

    document_id = serializers.UUIDField(required=False)
    position_type_name = serializers.CharField()

    class Meta:
        model = Position
        fields = (
            "document_id",
            "position_name",
            "position_type_name",
        )

    def validate_position_name(self, value: str) -> str:
        if len(value) < 1:
            raise serializers.ValidationError
        for char in value:
            if char not in self.SYMBOLS:
                raise serializers.ValidationError
        return value


class GetResumeSerializer(serializers.Serializer):
    document_id = serializers.UUIDField()
    email = serializers.EmailField()
