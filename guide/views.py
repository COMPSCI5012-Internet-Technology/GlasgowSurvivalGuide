from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    """Placeholder index view; replace with data-driven view when models and templates are added."""
    return HttpResponse("Glasgow Survival Guide – index.")


def about(request):
    """Placeholder about view."""
    return HttpResponse("Glasgow Survival Guide – about.")
