from rest_framework import serializers
from app2.models import Address


class CreateAddressSerializer(serializers.ModelSerializer):
    class Meta:
        fields=["line","city"]
        model=Address

    def validate(self,attrs):
        allowed=set(self.fields.keys())
        collected=set(self.initial_data.keys())
        unknown=collected-allowed
        if unknown:
            raise serializers.ValidationError(
                {key: f"Invalid data : {key}" for key in unknown}
            )
        return attrs

    

class GetAddressSerializer(serializers.ModelSerializer):
    class Meta:
        fields=["id","line","city"]
        model=Address

class UpdateAddressSerializer(serializers.ModelSerializer):
    class Meta:
        fields=["id","line","city"]
        model=Address
        
    def validate(self,attrs):
        allowed=set(self.fields.keys())
        collected=set(self.initial_data.keys())
        unknown = collected-allowed
        if unknown :
            raise serializers.ValidationError(
                {
                    key:f"Invalid data : {key}" for key in unknown
                }
            )
        return attrs