from django.contrib import admin
from django.urls import path
from . import views

app_name="Football Manager"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.TableView.as_view(), name="Table"),
    path("table/", views.TableView.as_view(), name="Table"),
    path("footballers/", views.FootballersView.as_view(), name="Footballers"),
    path("matches/", views.MatchesView.as_view(), name="Matches"),
    path("queue/", views.QueueView.as_view(), name="Queue"),
    path("statistics/", views.StatisticView.as_view(), name="Statistic"),
]
