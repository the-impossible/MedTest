from django.urls import path

app_name = "auth"

from MedTest_auth.views import  (
    DashboardView,

    LoginView,
    LogoutView,

    ManageStudentAccount,
    StudentDeleteView,
    StudentAccountView,

    ManageTest,
    ScheduleTestView,
    DeleteScheduleView,

    UploadTestResultView,
    ManageTestResults,
    UpdateTestResultView,
    DeleteTestResultView,

    ViewTest,
)

urlpatterns = [
    path('dashboard', DashboardView.as_view(), name="dashboard"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),

    # Hospital
    path('manage_student/', ManageStudentAccount.as_view(), name="manage_student"),
    path('delete_student/<str:pk>/', StudentDeleteView.as_view(), name="delete_student"),
    path('create_student/', StudentAccountView.as_view(), name="create_student"),

    path('manage_test/', ManageTest.as_view(), name="manage_test"),
    path('schedule_test/', ScheduleTestView.as_view(), name="schedule_test"),
    path('delete_test/<str:pk>/', DeleteScheduleView.as_view(), name="delete_test"),


    path('upload_test/<str:stud_id>/<str:test_id>', UploadTestResultView.as_view(), name="upload_test"),
    path('manage_results/', ManageTestResults.as_view(), name="manage_results"),
    path('update_result/<str:pk>', UpdateTestResultView.as_view(), name="update_result"),
    path('delete_result/<str:pk>', DeleteTestResultView.as_view(), name="delete_result"),

    # Students
    path('view_test/', ViewTest.as_view(), name="view_test"),

]
