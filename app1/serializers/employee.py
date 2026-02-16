from rest_framework import serializers
from app1.models import Employee

class CreateEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Employee
        fields=["name","email","salary","department","address","tags"]
        
    def validate_tags(self,value):
        if not isinstance(value,list):
            raise serializers.ValidationError("Tags must be a list of strings.")
        if not value or len(value)==0:
            raise serializers.ValidationError("At least one tag is required.")
        return value