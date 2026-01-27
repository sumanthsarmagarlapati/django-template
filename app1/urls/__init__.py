from django.urls import include, path


urlpatterns=[
    path('department/',include('app1.urls.department')),
    path('dashboard/',include('app1.urls.dashboard')),
    # path("employee",include('app1.urls.employee'))
]