from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import ujson

from symptom_checker.includes.description_parsing import get_symptoms, get_diseases


# disable CRSF validation
@csrf_exempt
def index(request):
    if request.method == "POST":

        description = request.POST.get("description")

        if description is None or description == "":

            return HttpResponse(
                ujson.dumps({"error": "nonempty 'description' field required."}),
                content_type="application/json",
                status=400,
            )

        symptoms = get_symptoms(description)

        diseases = get_diseases(symptoms)

        return HttpResponse(
            ujson.dumps({"symptoms": symptoms, "diseases": diseases}),
            content_type="application/json",
        )

    else:
        return HttpResponse(
            ujson.dumps(
                {"error": "Invalid request method. Only POST requests allowed."}
            ),
            content_type="application/json",
            status=405,
        )
