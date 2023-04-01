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

admin.site.register(User, UserAdmin)
admin.site.register(Programme)
admin.site.register(Session)
admin.site.register(Department)
admin.site.register(College)
admin.site.register(StudentProfile)