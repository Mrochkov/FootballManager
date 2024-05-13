from django.contrib import admin
from django.urls import path
from . import views

app_name = "football_manager"

urlpatterns = [
    path("admin/", admin.site.urls),
    path('login', views.custom_login, name='login'),
    path('logout', views.custom_logout, name='logout'),
    path("", views.TableView.as_view(), name="Table"),
    path("table/", views.TableView.as_view(), name="Table"),
    path("teams/", views.TeamsView.as_view(), name="Teams"),
    path("footballers/", views.FootballersView.as_view(), name="Footballers"),
    path("matches/", views.MatchesView.as_view(), name="Matches"),
    path("queue/", views.QueueView.as_view(), name="Queue"),
    path("statistics/", views.StatisticView.as_view(), name="Statistic"),
    path("add_footballer/", views.Add_Footballer, name="Add footballer"),
    path("add_team/", views.Add_Team, name="Add team"),
    path("add_match/", views.Add_Match, name="Add match"),
    path("add_to_queue/<int:queue_id>/", views.Add_to_queue, name="Add to queue"),

]
