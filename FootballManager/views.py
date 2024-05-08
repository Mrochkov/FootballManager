from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Footballer, Team, Match, Queue, Statistic
from .forms import FootballerForm


class TableView(generic.ListView):
    template_name = "FootballManager/table.html"
    context_object_name = "teams"

    def get_queryset(self):
        teams = Team.objects.all()
        for team in teams:
            team.points = team.wins * 3 + team.draws
            team.goals_balance = team.goals_scored - team.goals_lost
        return teams

    
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
    
#class AddFootballerView(generic.CreateView):
 #   form = FootballerForm()
  #  template_name = "FootballManager/add_footballer.html"
   # context = {'form': form}
#
#    def get_queryset(self, form):
#       return super().form_valid(form)
    
def Add_Footballer(request):
    form = FootballerForm()

    if request.method == 'POST':
        form = FootballerForm(request.POST)
        if form.is_valid():
            form.save()
            return FootballersView.as_view()
    template_name = "FootballManager/add_footballer.html"
    context = {'form': form}
    return render(request, template_name, context)