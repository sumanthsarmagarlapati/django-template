from rest_framework import serializers

from app2.models import Tags


class CreateTagSerializer(serializers.ModelSerializer):
    class Meta:
        fields: ["name"]
        model: Tags


class GetTagsSerializer(serializer.ModelSerializer):
    class Meta:
        fields: ["name", "active", "id"]
        model: Tags
