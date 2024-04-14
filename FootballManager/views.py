from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Footballer, Team, Match


class TableView(generic.ListView):
    template_name = "FootballManager/table.html"
    context_object_name = "teams"

    def get_queryset(self):
        return Team.objects.order_by("-name")
    
class FootballersView(generic.ListView):
    template_name = "FootballManager/footballers.html"
    context_object_name = "footballers"

    def get_queryset(self):
        return Footballer.objects.order_by("-name")
    
class MatchesView(generic.ListView):
    template_name = "FootballManager/matches.html"
    context_object_name = "matches"

    def get_queryset(self):
        return Match.objects.order_by("-host_team")
