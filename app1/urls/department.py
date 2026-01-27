from django.urls import path

from app1.views.department import createDepartment, getDepartmentDetails,updateDepartmentDetails

urlpatterns = [
    path("create", createDepartment, name="create_department"),
    path("update/<int:id>", updateDepartmentDetails, name="update_department"),
    path("", getDepartmentDetails, name="get_departments"),
]
