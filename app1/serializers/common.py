from rest_framework import serializers


class CommonPaginationSerializer(serializers.Serializer):
    page = serializers.IntegerField(required=False, min_value=1, default=1)
    limit = serializers.IntegerField(
        required=False, min_value=1, max_value=100, default=10
    )
    search = serializers.CharField(required=False, allow_blank=True)
    order_by = serializers.ChoiceField(
        required=False, choices=["id", "name", "active"], default="id"
    )
    order = serializers.ChoiceField(
        required=False, choices=["asc", "desc"], default="asc"
    )
    active = serializers.BooleanField(default=True)

    def validate(self, attrs):
        print(self.initial_data)
        allowed = set(self.fields.keys())
        collected = set(self.initial_data.keys())
        unknown = collected - allowed
        if unknown:
            raise serializers.ValidationError(
                {key: "Invalid Query Parameter" for key in unknown}
            )
        return attrs
