from django.urls import path

from app2.views import CreateAddress, GetAddresses, UpdateAddress

urlpatterns = [
    path("create", CreateAddress, name="create_address"),
    path("", GetAddresses, name="get_addresses"),
    path("update", UpdateAddress, name="update_address"),
]
