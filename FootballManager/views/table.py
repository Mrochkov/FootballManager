from django.views import generic
from django.db.models import F, Q
from django.db import models, transaction
from FootballManager.models import Team

class TableView(generic.ListView):
    template_name = "FootballManager/table.html"
    context_object_name = "teams"

    def get_queryset(self):
        teams = Team.objects.annotate(
            host_matches_count=models.Count('host_team', filter=Q(host_team__isnull=False)),
            guest_matches_count=models.Count('guest_team', filter=Q(guest_team__isnull=False)),
        )
        for team in teams:
            team.matches_count = team.host_matches_count + team.guest_matches_count
            team.points = team.wins * 3 + team.draws
            team.goals_balance = team.goals_scored - team.goals_lost
        return teams
