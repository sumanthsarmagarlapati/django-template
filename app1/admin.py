from django.contrib import admin

from app1.models.department_model import Department
from app1.models.employee_model import Employee, EmployeeTags


# --- Department Admin Configuration ---
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    # Columns to show in the main list view
    list_display = ("id", "name", "meta")
    # Adds a search bar that looks through the 'name' field
    search_fields = ("name",)
    # Adds a filter sidebar on the right side
    list_filter = ("name",)


# --- Employee Tags "Inline" Configuration ---
# This allows editing Tags directly inside the Employee's edit page
# StackedInline also there means TabularInline (Horizontal Layout) ands StackedInline (Vertical Layout) in just visual representation purpose only
class EmployeeTagInline(admin.TabularInline):
    model = EmployeeTags
    extra = 1  # Shows 1 blank row at the bottom to add a new tag quickly
    fields = ("tag", "active")  # Only show these specific fields in the inline

    # Allows the section to be minimized/expanded to save screen space in EmployeeTags add section
    classes = ["collapse"]


# --- Employee Admin Configuration ---
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    # Primary columns shown in the Employee list
    list_display = ("id", "name", "email", "salary", "department", "active")
    # Quick filters for the sidebar
    list_filter = ("department", "active")
    # Searchable fields (Name and Email)
    search_fields = ("name", "email")
    # Attaches the 'EmployeeTagInline' defined above to this page
    inlines = [EmployeeTagInline]


# --- EmployeeTags (Relationship Table) Admin Configuration ---
@admin.register(EmployeeTags)
class EmployeeTagsAdmin(admin.ModelAdmin):
    # Note: To see names instead of IDs here, use display_employee_name in list_display
    list_display = ("id", "employee", "tag", "active")

    # Filter the list by these categories
    list_filter = ("active", "employee__name", "tag__name")

    # CRITICAL: Search fields for relationships must use the double underscore __
    search_fields = ("id", "employee__name", "tag__name")

    # CUSTOM DISPLAY METHOD: Shows the Employee's 'name' instead of their ID
    @admin.display(ordering="employee__name", description="Employee Name")
    def display_employee_name(self, obj):
        return obj.employee.name

    # CUSTOM DISPLAY METHOD: Shows the Tag's 'name' instead of its ID
    @admin.display(ordering="tag__name", description="Tag Name")
    def display_tag_name(self, obj):
        return obj.tag.name
