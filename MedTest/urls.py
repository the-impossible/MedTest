from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", include("MedTest_basic.urls", namespace="basic")),
    path("admin/", admin.site.urls),
    path("auth/", include("MedTest_auth.urls", namespace="auth") ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_header = "Medical Test Scheduler "
admin.site.site_title = "Medical Test Scheduler "
admin.site.index_title = "Welcome to Medical Test Scheduler "