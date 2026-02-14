from app2.views import CreateTag, GetTags, UpdateTag
from django.urls import include,path

urlpatterns = [
    path("create", CreateTag, name="create_tag"),
    path("", GetTags, name="get_tags"),
    path("update", UpdateTag, name="update_tag"),
]
