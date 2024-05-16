from django.urls import path
from django.contrib import admin
from .views.table import TableView
from .views.teams import TeamsView, Add_Team, Info_Team, Edit_Team, Delete_Team
from .views.footballers import FootballersView, Add_Footballer
from .views.matches import  MatchesView, Add_Match, Add_Match_Result, Delete_Match
from .views.queues import QueueView, Add_to_queue
from .views.statistics import StatisticView
from .views.auth import custom_login, custom_logout

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', TableView.as_view(), name='Table'),
    path('table/', TableView.as_view(), name='Table'),
    path('teams/', TeamsView.as_view(), name='Teams'),
    path('teams/add/', Add_Team, name='Add Team'),
    path('teams/info/<int:team_id>/', Info_Team, name='Info team'),
    path('teams/edit/<int:team_id>/', Edit_Team, name='Edit team'),
    path('teams/delete/<int:team_id>/', Delete_Team, name='Delete team'),
    path('footballers/', FootballersView.as_view(), name='Footballers'),
    path('footballers/add/', Add_Footballer, name='Add Footballer'),
    path('matches/', MatchesView.as_view(), name='Matches'),
    path('matches/add/', Add_Match, name='Add Match'),
    path('matches/result/<int:match_id>/', Add_Match_Result, name='Add match result'),
    path('matches/delete/<int:match_id>/', Delete_Match, name='Delete match'),
    path('queue/', QueueView.as_view(), name='Queue'),
    path('queue/add/<int:queue_id>/', Add_to_queue, name='Add to queue'),
    path('statistics/', StatisticView.as_view(), name='Statistics'),
    path('login/', custom_login, name='Login'),
    path('logout/', custom_logout, name='Logout'),
]
