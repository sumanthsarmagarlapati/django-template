from rest_framework import serializers, status
from rest_framework.decorators import api_view
from app1.serializers.common import CommonPaginationSerializer
from app1.serializers.employee import CreateEmployeeSerializer, GetEmployeeSerializer
from rest_framework.response import Response
from app1.models import Employee, EmployeeTags
from django.db import transaction
from django.db import connection
from app2.serializers.tags import GetTagsSerializer

@api_view(["POST"])
def CreateEmployee(request):
    try:
        createSerializer=CreateEmployeeSerializer(data=request.data)
        if not createSerializer.is_valid():
            return Response(
                {"message": "Invalid data", "errors": createSerializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        print("Validated data:", createSerializer.validated_data)
        with transaction.atomic(): # Ensure either everything saves or nothing does            employee=Employee.create(**createSerializer.validated_data)
            validated_data = createSerializer.validated_data
            tags = validated_data.pop("tags", []) 
            print("Tags to be associated:", tags)
            employee=Employee.objects.create(**validated_data)
            # 1. Save each to the database in multiple queries (inefficient)
            # for tag in tags:
            #     EmployeeTags.create(employee=employee,tag=tag,active=True)

            # 2. Save all of them to the database in ONE single query\
            
            tags_data=[
                EmployeeTags(employee=employee,tag=tag_obj ,active=True)
                for tag_obj  in tags
            ]
            print("Tags data for bulk create:", tags_data)
            EmployeeTags.objects.bulk_create(tags_data)
            # employee=createSerializer.save()
            return Response(
                {"message": "Employee created successfully", "employee_id": employee.id},
                status=status.HTTP_201_CREATED,
            )
    except Exception as e:
        return Response(
            {"message": "Employee creation failed", "error": str(e)},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["GET"])
def GetEmployees(request):
    try:
        paginationSerializer=CommonPaginationSerializer(data=request.query_params)
        if not paginationSerializer.is_valid(raise_exception=True):
            return Response({"message":"Invalid data","error":paginationSerializer.errors},status=status.HTTP_400_BAD_REQUEST)
        
        employee=Employee.objects.all()
        # employee=employee.select_related("department","address").prefetch_related("tags")
        page=paginationSerializer.validated_data.get("page")
        limit=paginationSerializer.validated_data.get("limit")
        search=paginationSerializer.validated_data.get("search")
        order=paginationSerializer.validated_data.get("order")
        order_by=paginationSerializer.validated_data.get("order_by")
        
        if "active" in paginationSerializer.validated_data:
            employee=employee.filter(active=paginationSerializer.validated_data.get("active"))
            
        start=(page-1)*limit
        end = start+limit
        if search:
            employee=employee.filter(name__icontains=search)
        
        employee=employee.order_by(order_by if order.lower()=="asc" else f"-{order_by}")
        total=employee.count()
        paginated_records=employee.distinct()[start:end]
        serialized_data=GetEmployeeSerializer(paginated_records,many=True).data  
        print(f"Number of queries: {len(connection.queries)}")
        for query in connection.queries:
            print(f"SQL: {query['sql']}\n")
        return Response(
            {
                "data":serialized_data,
                "count":total,
            },status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error":str(e)},status=status.HTTP_400_BAD_REQUEST)
        
        
@api_view(["UPDATE"])
def UpdateEmployee(request,id):
    try:
        employee=Employee.documents.get(id=id)
        updateSerializer=CreateEmployeeSerializer(employee,data=request.data,partial=True)
        if not updateSerializer.is_valid():
            return Response(
                {"message": "Invalid data", "errors": updateSerializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
    except Exception as e:
        return Response({"error":str(e)},status=status.HTTP_400_BAD_REQUEST)