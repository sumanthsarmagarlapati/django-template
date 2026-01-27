import json

from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view

from app1.models.department_model import Department
from app1.serializers.common import CommonPaginationSerializer
from app1.serializers.department import (
    CreateDepartmentSerializer,
    GetDepartmentSerializer,
)


@api_view(["POST"])
def createDepartment(request):
    try:
        departmentSerializer = CreateDepartmentSerializer(data=request.data)
        if not departmentSerializer.is_valid():
            return JsonResponse(
                {"message": "Creation Failed", "error": departmentSerializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        Department.objects.create(
            name=departmentSerializer.validated_data["name"],
            meta=departmentSerializer.validated_data.get("meta", {}),
        )
        return JsonResponse({"message": "Department created successfully"}, status=201)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@api_view(["GET"])
def getDepartmentDetails(request):
    try:
        querySerializer=CommonPaginationSerializer(data=request.query_params)
        querySerializer.is_valid(raise_exception=True)   
        params=querySerializer.validated_data
        print("request.query_params:", request.query_params)
        print("dict:", request.query_params.dict())
        
        departments = Department.objects.all()
        getDepartments = GetDepartmentSerializer(departments, many=True)
        return JsonResponse(
            {
                "data": getDepartments.data,
                "message": "Data Fetched",
                "status": status.HTTP_200_OK,
            },
            status=status.HTTP_200_OK,
        )
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@api_view(["PATCH"])
def updateDepartmentDetails(request, id):
    print("IDDDDDDDDDDDDDDDDDDDDDDDD",id)
    try:
        department = Department.objects.get(id=id)

        updatedSerilizer = CreateDepartmentSerializer(department,data=request.data,partial=True)
        if not updatedSerilizer.is_valid():
            return JsonResponse(
                {
                    "message": "Validation failed",
                    "errors": updatedSerilizer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )
            
        Department.objects.filter(id=id).update(**updatedSerilizer.validated_data)
        
        return JsonResponse({"message": "Department updated successfully"}, status=201)

    except Exception as e:
        return JsonResponse(
            {
                "message": "Updtion failed",
                "error": e,
                "status": status.HTTP_400_BAD_REQUEST,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
