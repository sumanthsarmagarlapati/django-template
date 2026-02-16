from django.urls import path,include
from app1.views import CreateEmployee

urlpatterns=[
    path("create",CreateEmployee,name="create_employee"),
    path("create",GetEmployees,name="create_employee"),
    path("create",UpdateEmployee,name="create_employee"),
]