from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


# Register your models here.
from MedTest_auth.models import *

class UserAdmin(UserAdmin):
    list_display = ('username', 'name',  'pic', 'date_joined', 'last_login', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('username','name')
    ordering = ('username',)
    readonly_fields = ('date_joined', 'last_login',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class StudentProfileAdmin(UserAdmin):
    list_display = ('user_id', 'department', 'gender', 'age', 'session', 'is_completed', 'college', 'date_created')
    search_fields = ('user_id__username','department__dept_title', 'gender__title', 'session__session_title')
    ordering = ('user_id',)
    readonly_fields = ('date_created',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(User, UserAdmin)
admin.site.register(Session)
admin.site.register(Department)
admin.site.register(College)
admin.site.register(StudentProfile, StudentProfileAdmin)
admin.site.register(AmountToSchedule)
admin.site.register(ScheduleTest)
admin.site.register(Gender)
admin.site.register(BloodGroup)
admin.site.register(TestResult)
admin.site.register(Sickling)