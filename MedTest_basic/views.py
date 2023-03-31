from django.shortcuts import render
from django.views.generic.base import TemplateView

# My App imports


# Create your views here.

class HomeView(TemplateView):
    template_name = "basic/index.html"
