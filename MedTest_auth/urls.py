from django.urls import path

app_name = "auth"

from MedTest_auth.views import  (
    DashboardView,
)

urlpatterns = [
    path('dashboard', DashboardView.as_view(), name="dashboard"),
]
