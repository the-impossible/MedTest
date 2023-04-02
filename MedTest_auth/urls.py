from django.urls import path

app_name = "auth"

from MedTest_auth.views import  (
    DashboardView,

    LoginView,
    LogoutView,

    ManageStudentAccount,
    StudentDeleteView,
    StudentAccountView,
)

urlpatterns = [
    path('dashboard', DashboardView.as_view(), name="dashboard"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),

    path('manage_student/', ManageStudentAccount.as_view(), name="manage_student"),
    path('delete_student/<str:pk>/', StudentDeleteView.as_view(), name="delete_student"),
    path('create_student/', StudentAccountView.as_view(), name="create_student"),

]
