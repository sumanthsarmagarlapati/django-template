from rest_framework.decorators import api_view
from rest_framework import status
from app2.serializers import CreateAddressSerializer,GetAddressSerializer,UpdateAddressSerializer
from app2.models import Address
from django.http import JsonResponse

@api_view(["POST"])
def CreateAddress(request):
    try:
        createSerializer=CreateAddressSerializer(data=request.data)
        if not createSerializer.is_valid():
            return JsonResponse({"message":"Creation Failed","error":createSerializer.errors},
            status=status.HTTP_400_BAD_REQUEST)

        # createSerializer.save()    // can use directly
        print("createSerializer s",createSerializer.validated_data)

        Address.objects.create(
            line=createSerializer.validated_data.get("line"),
            city=createSerializer.validated_data.get("city"),
        )
        return JsonResponse({"message":"Creation Successful"},status=201)

    except Exception as e:
        return JsonResponse({"error":str(e)},status=500)


@api_view(["GET"])
def GetAddresses(request):
    try:
        print("")
    except Exception as e :
        return  JsonResponse({'error':str(e)},status=500)

@api_view(["UPDATE"])
def UpdateAddress(request):
    try:
        print("")
    except Exception as e:
        return JsonResponse({"error":str(e)},status=400)