from rest_framework import serializers
from resume.models import Position


class ShowPositionTypesSerializer(serializers.Serializer):
    document_id = serializers.UUIDField(required=False)
    position_types = serializers.ListField(child=serializers.CharField())


class ShowIndustriesSerializer(serializers.Serializer):
    document_id = serializers.UUIDField(required=False)
    position_name = serializers.CharField()
    industries = serializers.ListField(child=serializers.CharField())


class ShowCompetenciesSerializer(serializers.Serializer):
    document_id = serializers.UUIDField()
    position_name = serializers.CharField()
    industry = serializers.CharField()
    leader_competencies = serializers.ListField(
        child=serializers.CharField(), required=False
    )
    general_competencies = serializers.ListSerializer(child=serializers.CharField())
    professional_competencies = serializers.ListSerializer(
        child=serializers.CharField()
    )


class CreatePositionSerializer(serializers.ModelSerializer):
    document_id = serializers.UUIDField(required=False)
    position_type_name = serializers.CharField()

    class Meta:
        model = Position
        fields = (
            "document_id",
            "position_name",
            "position_type_name",
        )
