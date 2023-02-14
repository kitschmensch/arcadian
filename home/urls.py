# HOME URLS
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("api/", include("entities.urls")),
    path("", TemplateView.as_view(template_name="../templates/index.html")),
    path("upload/", TemplateView.as_view(template_name="../templates/upload.html")),
]
