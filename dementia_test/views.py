from django.http import JsonResponse
from .models import DementiaTestCase


def create_new_test(request):
    return JsonResponse({"id": DementiaTestCase.objects.create().id})
