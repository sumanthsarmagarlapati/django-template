import json

from django.db.models import Q, TextField
from django.db.models.functions import Cast
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view

from app1.models.department_model import Department
from app1.serializers.common import CommonPaginationSerializer
from app1.serializers.department import (
    CreateDepartmentSerializer,
    GetDepartmentSerializer,
)


@api_view(["POST"])
def createDepartment(request):
    try:
        departmentSerializer = CreateDepartmentSerializer(data=request.data)
        if not departmentSerializer.is_valid():
            return JsonResponse(
                {"message": "Creation Failed", "error": departmentSerializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # departmentSerializer.save() // also there Centralizes validation + creation but for leraning purpose we use manual operations

        Department.objects.create(
            name=departmentSerializer.validated_data["name"],
            meta=departmentSerializer.validated_data.get("meta", {}),
        )
        return JsonResponse({"message": "Department created successfully"}, status=201)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@api_view(["GET"])
def getDepartmentDetails(request):
    try:
        querySerializer = CommonPaginationSerializer(data=request.query_params)
        querySerializer.is_valid(raise_exception=True)
        params = querySerializer.validated_data
        sort_field = params.get("order_by", "id")
        sort_direction = params.get("order", "asc")
        page = params.get("page")
        limit = params.get("limit")
        search = params.get("search")
        print("params", params)
        departments = Department.objects.all()
        departments = departments.filter(active=params.get("active", True))
        if sort_direction.lower() == "desc":
            sort_field = f"-{sort_field}"
        departments = departments.order_by(sort_field)
        if search:
            departments = (
                departments.annotate(meta_as_text=Cast("meta", TextField()))
                .filter(
                    Q(name__icontains=f"{search}")
                    | Q(meta_as_text__icontains=f"{search}")
                )
                .distinct()
            )

        start = (page - 1) * limit
        end = start + limit
        total_count = departments.count()
        paginated_records = departments[start:end]
        getDepartments = GetDepartmentSerializer(paginated_records, many=True)
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        return JsonResponse(
            {
                "data": getDepartments.data,
                "message": "Data Fetched",
                "status": status.HTTP_200_OK,
            },
            status=status.HTTP_200_OK,
        )
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@api_view(["PATCH"])
def updateDepartmentDetails(request, id):
    try:
        department = Department.objects.get(id=id)

        updatedSerializer = CreateDepartmentSerializer(
            department, data=request.data, partial=True
        )
        if not updatedSerializer.is_valid():
            return JsonResponse(
                {"message": "Validation failed", "errors": updatedSerializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 2. Let the serializer handle the update (Cleaner!)
        # updatedSerializer.save()
        print("updatedSerializer.validated_data", updatedSerializer.validated_data)

        # bad practice to filter for single record update becoz filter results list of matched records so all the records matched are updated but here we need single macthed record is updated
        # updated_count = Department.objects.filter(id=id).update(**updatedSerializer.validated_data)
        # if updated_count == 0:
        #     return JsonResponse({"error": "Nothing was updated"}, status=404)

        for key, value in updatedSerializer.validated_data.items():
            setattr(department, key, value)
        department.save()

        return JsonResponse({"message": "Department updated successfully"}, status=201)

    except Exception as e:
        return JsonResponse(
            {
                "message": "Updation failed",
                "error": str(e),
                "status": status.HTTP_400_BAD_REQUEST,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


#  Explanation of Pagination :
#           1. .all() will give list of django
#           2. Calling .all() is lazy, meaning it does not hit the database at that line. In Django, a QuerySet (like what .all() returns) can be passed around, filtered, and annotated as many times as you want without a single trip to the database.
#                departments = Department.objects.all() # 0 DB hits
#                departments = departments.filter(active=True) # 0 DB hits
#                departments = departments.annotate(...) # 0 DB hits
#             Django is just building the SQL string in the background during these steps.
#           3. When does it actually hit the DB?
#             The database is only contacted when you evaluate the QuerySet. This happens when:
#             - Slicing with a step: departments[0:10:2] (Standard slicing [0:10] is still lazy!)
#             - Iterating: for dept in departments:
#             - Counting: departments.count() <-- This hits the DB .
#             - Converting to a list: list(departments) <-- This hits db
#             - Serializing: When you pass it to GetDepartmentSerializer(...) and access .data.
#             - Checking existence: if departments.exists():
#             in this cases DB Hit happend in all otrher cases django frames single SQL query for overall lines
#           4. This "laziness" allows Django to be highly efficient. If you call .all() and then immediately add a .filter(), Django combines them into a single SQL query instead of fetching all records and filtering them in Python.
#           5. When we searching in JSON fields we cant search direactly either
#                 mention that specific field in json as in above example meta_role_icontains=search  and it works only if role field is mandatory in json
#                 otherwise do like in above example as make toatl json object into string using annotate
#                  .annotate() is like adding a temporary "virtual column" to your database results just for that specific query. It doesn't change your table in the database;
#                  it just calculates extra data on the fly. Django's annotate docs explain this as "attaching" attributes to each object.
#           6. there is nop direct order() FUNCTION IN ORM if we mention - before order_by field it means order that field in descending order otherwise ascending by default
#           7. In search name__icontains (i stands for in-sensitive) means partial search and if we mention
#              departments=departments.filter(Q(name=f"{search}") | Q(meta=f"{search}"))  like this its eaxct search
#           8. distinct() it will removes duplicate records from result for example
#                Imagine you are searching for the keyword "Admin" across two fields: name and meta__role.
#                ID	Name	Role (in Meta)
#                1	Admin User	Administrator
#                departments = Department.objects.filter(Q(name__icontains=search_term) | Q(meta__role__icontains=search_term))
#             The Result Without .distinct():The database finds "Admin" in the name column and in the meta__role column. Because both conditions are met, it may return ID 1 twice in your results.
#             Adding .distinct() ensures that the SQL query includes a SELECT DISTINCT statement, which tells the database to collapse those duplicate rows into a single unique record.
#           we should use .distinct() before db hit like departments.distinct()[start:end] is valid and departments.[start:end]distinct() is invalid becoz no use of using distinct after db hit gives error
#           9. GetDepartmentSerializer(paginated_records, many=True)
#              Single Object (many=False / Default): If you fetch one record (e.g., Department.objects.get(id=1)), the serializer expects a single dictionary-like object.
#              List of Objects (many=True): Since your paginated_records is a QuerySet (a list of multiple departments), you must set many=True. This tells the serializer to loop through the list and serialize each item individually, returning them as a JSON array []
#              AND If you pass paginated_records list as a input and  but forget many=True, Django will throw an AttributeError (usually saying 'QuerySet' object has no attribute 'name') because it tries to find the "name" field on the entire list instead of the items inside it
#         Pro-Tip: Because total_count and paginated_records hit the database separately, your code makes two database calls. This is normal for pagination.


# Explanation For Update :
# 1. department (The Instance)
#     By passing the existing department object as the first argument, you tell the serializer: "Don't create a new record. Use this existing record as the base for comparison and updating."
# 2. data=request.data (The Input)
#     This provides the new information the user sent (e.g., {"active": false}). The serializer will now compare this new data against the existing values in the department object.
# 3. partial=True (The "Magic" Switch)
#     This is the most important part for a PATCH request.
#     Without partial=True: The serializer expects all required fields (like name). If you only send active, it will fail with an error: "Name field is required."
#     With partial=True: It tells the serializer: "Only validate the fields that are actually present in request.data. Ignore any missing required fields."
# 4. What happens when you later call .save()?
#     Once you run serializer.is_valid(), DRF prepares a special version of the object. When you eventually call serializer.save():
# 5. serializer.validated_data.items() for update what happens internally
#    This takes the dictionary of cleaned data and turns it into pairs of (key, value).
#    Example: If the user sends {"name": "HR"}, this gives you ('name', 'HR').
#    2. setattr(department, attr, value)
#    setattr is a built-in Python function that stands for "set attribute".
#    It works like this: setattr(object, "variable_name", value) is exactly the same as writing object.variable_name = value.
