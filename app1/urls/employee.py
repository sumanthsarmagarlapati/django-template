from django.urls import  path

from app1.views import CreateEmployee, GetEmployees, UpdateEmployee

urlpatterns=[
    path("create",CreateEmployee,name="create_employee"),
    path("update/<int:id>",UpdateEmployee,name="create_employee"),
    path("",GetEmployees,name="create_employee"),
]