from rest_framework.decorators import api_view
from rest_framework import status
from app1.serializers import CommonPaginationSerializer
from app2.serializers import CreateAddressSerializer,GetAddressSerializer,UpdateAddressSerializer
from app2.models import Address
from rest_framework.response import Response
from django.db.models import Q

@api_view(["POST"])
def CreateAddress(request):
    try:
        createSerializer=CreateAddressSerializer(data=request.data)
        if not createSerializer.is_valid():
            return Response({"message":"Creation Failed","error":createSerializer.errors},
            status=status.HTTP_400_BAD_REQUEST)

        # createSerializer.save()    // can use directly
        print("createSerializer s",createSerializer.validated_data)

        Address.objects.create(
            line=createSerializer.validated_data.get("line"),
            city=createSerializer.validated_data.get("city"),
        )
        return Response({"message":"Creation Successful"},status=201)

    except Exception as e:
        return Response({"error":str(e)},status=500)


@api_view(["GET"])
def GetAddresses(request):
    try:
       paginationSerializer=CommonPaginationSerializer(data=request.query_params)
       if not paginationSerializer.is_valid():
            return Response({"message":"Invalid data","error":paginationSerializer.errors},status=400)
       address=Address.objects.all()
       page=paginationSerializer.validated_data.get("page")
       limit=paginationSerializer.validated_data.get("limit")
       search=paginationSerializer.validated_data.get("search")
       order=paginationSerializer.validated_data.get("order")
       order_by=paginationSerializer.validated_data.get("order_by")
       
       if "active" in paginationSerializer.validated_data:
           address=address.filter(active=paginationSerializer.validated_data.get("active"))
           
       start=(page-1)*limit
       end = start+limit
       if search:
           address=address.filter(Q(line__icontains=search) | Q(city__icontains=search) | Q(id__icontains=search))
       
       address=address.order_by(order_by if order.lower()=="asc" else f"-{order_by}")
       total=address.count()
       paginated_records=address.distinct()[start:end]
       serialized_data=GetAddressSerializer(paginated_records,many=True).data  
       
       return Response(
           {
               "data":serialized_data,
               "count":total,
           },status=status.HTTP_200_OK
       )
    except Exception as e :
        return  Response({'error':str(e)},status=500)
@api_view(["UPDATE"])
def UpdateAddress(request):
    try:
        print("")
    except Exception as e:
        return Response({"error":str(e)},status=400)