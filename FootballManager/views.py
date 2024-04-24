from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Footballer, Team, Match, Queue, Statistic


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


class QueueView(generic.ListView):
    template_name = "FootballManager/queue.html"
    context_object_name = "queues"

    def get_queryset(self):
        return Queue.objects.order_by("id")


class StatisticView(generic.ListView):
    template_name = "FootballManager/statistics.html"
    context_object_name = "statistics"

    def get_queryset(self):
        return Statistic.objects.order_by("-goals_scored")
