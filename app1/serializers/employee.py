from rest_framework import serializers
from app1.models import Employee
from app1.serializers.department import GetDepartmentSerializer
from app2.models import Tags
from app2.serializers.address import GetAddressSerializer
from app2.serializers.tags import GetTagsSerializer

class CreateEmployeeSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=Tags.objects.filter(active=True), 
        required=True
    )
    
    class Meta:
        model=Employee
        fields=["name","email","salary","department","address","tags"]
        
    def validate_tags(self,value):
        if not isinstance(value,list):
            raise serializers.ValidationError("Tags must be a list of strings.")
        if not value or len(value)==0:
            raise serializers.ValidationError("At least one tag is required.")
        return value
    
class GetEmployeeSerializer(serializers.ModelSerializer):
    department=GetDepartmentSerializer(read_only=True)
    address =GetAddressSerializer(read_only=True)
    tags =GetTagsSerializer(many=True,read_only=True)
    class Meta:
        model=Employee
        fields=["id","name","email","salary","department.name","address.name","tags"]
