

from rest_framework import serializers
from app1.models.department_model import Department

class CreateDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Department
        fields=["name","meta"]

class GetDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Department
        fields=["id","name","meta"]