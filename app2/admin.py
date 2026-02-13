from django.contrib import admin


from app2.models import Address
from app2.models import Tags

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display=("line","city")
    search_fields=("line",)
    list_filter=("line",)


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display=("active","name")
    list_filter=("name",)
    search_fields=("name",)