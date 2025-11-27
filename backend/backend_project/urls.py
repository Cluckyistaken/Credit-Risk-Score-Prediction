from django.contrib import admin
from django.urls import path, include
from .views import index

urlpatterns = [
    path("", index, name="index"),          # <--- root path added
    path("admin/", admin.site.urls),
    path("api/users/", include("apps.users.urls")),
    path("api/applications/", include("apps.applications.urls")),
    path("api/ml/", include("apps.ml.urls")),
]
