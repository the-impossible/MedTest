from django.urls import path

from MedTest_basic.views import (
    HomeView,
)

app_name = "basic"

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
]
