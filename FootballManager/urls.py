from django.urls import path
from .views.table import TableView
from .views.teams import TeamsView, Add_Team
from .views.footballers import FootballersView, Add_Footballer
from .views.matches import MatchesView, Add_Match, Add_Match_Result
from .views.queues import QueueView, Add_to_queue
from .views.statistics import StatisticView
from .views.auth import custom_login, custom_logout

urlpatterns = [
    path('', TableView.as_view(), name='Table'),
    path('table/', TableView.as_view(), name='Table'),
    path('teams/', TeamsView.as_view(), name='Teams'),
    path('teams/add/', Add_Team, name='Add Team'),
    path('footballers/', FootballersView.as_view(), name='Footballers'),
    path('footballers/add/', Add_Footballer, name='Add Footballer'),
    path('matches/', MatchesView.as_view(), name='Matches'),
    path('matches/add/', Add_Match, name='Add Match'),
    path('matches/result/<int:match_id>/', Add_Match_Result, name='Add match result'),
    path('queue/', QueueView.as_view(), name='Queue'),
    path('queue/add/<int:queue_id>/', Add_to_queue, name='Add to queue'),
    path('statistics/', StatisticView.as_view(), name='Statistics'),
    path('login/', custom_login, name='Login'),
    path('logout/', custom_logout, name='Logout'),
]
