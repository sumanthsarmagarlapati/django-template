from django.urls import path

from app1.views.dashboard import getDashboardBasic

urlpatterns = [
    path("basic", getDashboardBasic, name="get_dashboard_basic"),
]
