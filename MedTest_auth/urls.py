from django.urls import path

app_name = "auth"

from MedTest_auth.views import  (
    DashboardView,
    LoginView,
)

urlpatterns = [
    path('dashboard', DashboardView.as_view(), name="dashboard"),
    path('login/', LoginView.as_view(), name="login"),
]
