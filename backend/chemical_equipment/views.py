from django.http import JsonResponse

def api_root(request):
    return JsonResponse({
        "message": "Chemical Equipment API is running",
        "endpoints": {
            "admin": "/admin/",
            "api": "/api/"
        }
    })
