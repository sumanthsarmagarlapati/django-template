from rest_framework import serializers, status
from rest_framework.decorators import api_view
from app1.serializers.common import CommonPaginationSerializer
from app1.serializers.employee import CreateEmployeeSerializer
from rest_framework.response import Response

@api_view(["POST"])
def CreateEmployee(request):
    try:
        createSerializer=CreateEmployeeSerializer(data=request.data)
        if not createSerializer.is_valid():
            return Response(
                {"message": "Invalid data", "errors": createSerializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        tags=createSerializer.validated_data.get("tags",[])
        for tag in tags:
            employee_tags=
        print("Creating employee with data:", createSerializer.validated_data)
        employee=createSerializer.save()
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
        paginationSerializer=CommonPaginationSerializer(request.query_params)
    except Exception as e:
        return Response({"error":str(e)},status=status.HTTP_400_BAD_REQUEST)
        
        
@api_view(["UPDATE"])
def UpdateEmployee(request):
    try:
    except Exception as e:
        return Response({"error":str(e)},status=status.)