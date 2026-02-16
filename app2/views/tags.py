from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from app1.serializers import CommonPaginationSerializer
from app2.serializers import CreateTagSerializer
from app2.models import Tags
from app2.serializers.tags import GetTagsSerializer

@api_view(["POST"])
def CreateTag(request):
    try:
        createSerializer=CreateTagSerializer(data=request.data)
        if not createSerializer.is_valid():
            return  Response({"message":"Creation Failed","error":createSerializer.errors},status=status.HTTP_400_BAD_REQUEST)
        Tags.objects.create(**createSerializer.validated_data)
        return Response({"message":"Creation Successful"},status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({"error":str(e),status:500})


@api_view(["GET"])
def GetTags(request):
    try:
        paginationSerializer=CommonPaginationSerializer(data=request.query_params)
        if not paginationSerializer.is_valid(raise_exception=True):
            return Response({"message":"Invalid data","error":paginationSerializer.errors},status=status.HTTP_400_BAD_REQUEST)
        
        tags=Tags.objects.all()
        page=paginationSerializer.validated_data.get("page")
        limit=paginationSerializer.validated_data.get("limit")
        search=paginationSerializer.validated_data.get("search")
        order=paginationSerializer.validated_data.get("order")
        order_by=paginationSerializer.validated_data.get("order_by")
        
        if "active" in paginationSerializer.validated_data:
            tags=tags.filter(active=paginationSerializer.validated_data.get("active"))
            
        start=(page-1)*limit
        end = start+limit
        if search:
            tags=tags.filter(name__icontains=search)
        
        tags=tags.order_by(order_by if order.lower()=="asc" else f"-{order_by}")
        total=tags.count()
        paginated_records=tags.distinct()[start:end]
        serialized_data=GetTagsSerializer(paginated_records,many=True).data  
        
        return Response(
            {
                "data":serialized_data,
                "count":total,
            },status=status.HTTP_200_OK
        )
    except Exception as e :
        return  Response({'error':str(e)},status=500)

@api_view(["UPDATE"])
def UpdateTag(request):
    try:
        print("")
    except Exception as e:
        return Response({"error":str(e),status:400})