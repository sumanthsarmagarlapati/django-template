from rest_framework.decorators import api_view
from .

@api_view(["POST"])
def createTag(request):
    try:
        tagSerializer=CreateTagSerializer()
    except Exception as e:
        return JsonResponse({"error":str(e),status:500})