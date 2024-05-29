from django.views import generic
from django.db.models import F, Q, Count
from django.db import models
from FootballManager.models import Team

class TableView(generic.ListView):
    template_name = "FootballManager/table.html"
    context_object_name = "teams"

    def get_queryset(self):
        teams = Team.objects.annotate(
            host_matches_count=Count('host_team', filter=Q(host_team__isnull=False)),
            guest_matches_count=Count('guest_team', filter=Q(guest_team__isnull=False)),
            matches_count=F('host_matches_count') + F('guest_matches_count'),
            points=F('wins') * 3 + F('draws'),
            goals_balance=F('goals_scored') - F('goals_lost')
        ).order_by('-points')
        return teams
