from django.contrib import admin
from django.urls import path
from . import views

app_name="Football Manager"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("table/", views.TableView.as_view(), name="Table"),
    path("", views.dashboard, name="dashboard"),
]
