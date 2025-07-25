from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return HttpResponse(
        "<h1>Welcome to Gratitude Journal!</h1>"
        "<p>Your personal space for daily gratitude entries.</p>"
    )
