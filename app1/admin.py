from django.contrib import admin

from app1.models.department_model import Department
from app1.models.employee_model import Employee, EmployeeTags


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "meta")
    search_fields = ("name",)
    list_filter = ("name",)


class EmployeeTagInline(admin.TabularInline):
    model = EmployeeTags
    extra = 1


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "salary", "department", "active")
    list_filter = ("department", "active")
    search_fields = ("name", "email")
    inlines = [EmployeeTagInline]
