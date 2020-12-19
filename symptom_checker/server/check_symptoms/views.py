from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import ujson


@csrf_exempt
def index(request):
    if request.method == "POST":
        return HttpResponse(
            ujson.dumps({"status": "ok"}),
            content_type="application/json",
        )

    else:
        return HttpResponse(
            ujson.dumps(
                {"Error": "Invalid request method. Only POST requests allowed."}
            ),
            content_type="application/json",
            status=405,
        )
