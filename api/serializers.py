from rest_framework import serializers
from .models import Case, Evidence, Section


class EvidenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evidence
        fields = "__all__"


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = "__all__"


class CaseSerializer(serializers.ModelSerializer):
    # evidences = EvidenceSerializer(many=True)
    # sections = SectionSerializer(many=True)

    class Meta:
        model = Case
        fields = "__all__"

    def create(self, validated_data):

        # evidences = validated_data.pop("evidences")
        # sections = validated_data.pop("sections")

        case = Case.objects.create(**validated_data)

        # for evidence in evidences:
        #     Evidence.objects.create(**evidence, case=case)

        # for section in sections:
        #     Section.objects.create(**section, case=case)

        return case
