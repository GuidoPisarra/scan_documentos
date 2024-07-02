from django.contrib import admin
from django.urls import path, include
from AppScan import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("scan", views.scan, name="scan"),
    path("scan_archivo", views.scan_archivo, name="scan_archivo"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
