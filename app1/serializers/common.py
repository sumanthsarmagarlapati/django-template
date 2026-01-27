from rest_framework  import serializers

class CommonPaginationSerializer(serializers.Serializer):
    class Meta:
        page=serializers.IntegerField(required=False,min_value=1,default=1)
        limit=serializers.IntegerField(required=False,min_value=1,max_value=100,default=10)
        serach=serializers.CharField(required=False,allow_blank=True)
        order_by=serializers.ChoiceField(
            required=False,
            choices=["id","name","active"],
            default="id"
        )
        order=serializers.ChoiceField(required=False,choices=["asc","desc"],default="asc")
        active=serializers.BooleanField(default=True)