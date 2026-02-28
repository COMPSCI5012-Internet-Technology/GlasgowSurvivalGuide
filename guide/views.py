from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, 'guide/index.html')


def about(request):
    """Placeholder about view."""
    return HttpResponse("Glasgow Survival Guide – about.")
