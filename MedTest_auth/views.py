from django.shortcuts import render
from django.views.generic.base import TemplateView


# Create your views here.

class DashboardView(TemplateView):
    template_name = "auth/dashboard.html"
