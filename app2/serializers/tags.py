from rest_framework import serializers
from app2.models import Tags


class CreateTagSerializer(serializers.ModelSerializer):
    class Meta:
        fields= ["name"]
        model= Tags


class GetTagsSerializer(serializers.ModelSerializer):
    class Meta:
        fields= ["name", "active", "id"]
        model= Tags


class UpdateTagSerializer(serializers.ModelSerializer):
    class Meta:
        fields= ["name", "active"]
        model= Tags
