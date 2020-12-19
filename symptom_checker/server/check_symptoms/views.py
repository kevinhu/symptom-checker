from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import ujson

from symptom_checker.includes.description_parsing import get_symptoms, get_diseases


VALID_MIN_FREQUENCIES = [
    "Very rare",
    "Occasional",
    "Frequent",
    "Very frequent",
    "Obligate",
]

VALID_SORT_METHODS = ["num_matched_symptoms", "first_matched_symptom"]


# disable CRSF validation
@csrf_exempt
def index(request):
    if request.method == "POST":

        description = request.POST.get("description")
        min_frequency = request.POST.get("min_frequency")
        sort_method = request.POST.get("sort_method")

        if description is None or description == "":

            return HttpResponse(
                ujson.dumps({"error": "nonempty 'description' field required."}),
                content_type="application/json",
                status=400,
            )

        if min_frequency is None:
            min_frequency = "Very rare"

        if min_frequency not in VALID_MIN_FREQUENCIES:

            error = f"invalid 'min_frequency' field. Possible options in order of exclusivity: {VALID_MIN_FREQUENCIES}"

            return HttpResponse(
                ujson.dumps({"error": error}),
                content_type="application/json",
                status=400,
            )

        if sort_method not in VALID_SORT_METHODS:

            error = (
                f"invalid 'sort_method' field. Possible options: {VALID_SORT_METHODS}"
            )

            return HttpResponse(
                ujson.dumps({"error": error}),
                content_type="application/json",
                status=400,
            )

        symptoms = get_symptoms(description)

        diseases = get_diseases(symptoms, min_frequency, sort_method)

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
