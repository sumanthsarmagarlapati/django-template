from rest_framework.decorators import api_view

@api_view(["POST"])
def CreateTag(request):
    try:
        print("")

    except Exception as e:
        return JsonResponse({"error":str(e),status:500})


@api_view(["GET"])
def GetTags(request):
    try:
        print("")
    except Exception as e :
        return  JsonResponse({'error':str(e),status:500})

@api_view(["UPDATE"])
def UpdateTag(request):
    try:
        print("")
    except Exception as e:
        return JsonResponse({"error":str(e),status:400})