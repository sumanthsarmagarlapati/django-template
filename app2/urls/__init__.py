from django.urls import include,path


urlpatterns=[
    path('address/',include('app2.urls.address')),
    path('tags/',include('app2.urls.tags')),
]