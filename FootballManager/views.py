from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.views.decorators.http import require_POST
from django.contrib import messages


from .models import Footballer, Team, Match, Queue, Statistic
from .forms import FootballerForm
from .forms import TeamForm
from .forms import MatchForm
from .forms import QueueForm


class TableView(generic.ListView):
    template_name = "FootballManager/table.html"
    context_object_name = "teams"

    def get_queryset(self):
        teams = Team.objects.all()
        for team in teams:
            team.points = team.wins * 3 + team.draws
            team.goals_balance = team.goals_scored - team.goals_lost
        return teams
    

class TeamsView(generic.ListView):
    template_name = "FootballManager/teams.html"
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
    

def Add_Footballer(request):
    form = FootballerForm()

    if request.method == 'POST':
        form = FootballerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Footballers')
    template_name = "FootballManager/add_footballer.html"
    context = {'form': form}
    return render(request, template_name, context)


def Add_Team(request):
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Teams')
    else:
        form = TeamForm()

    context = {'form': form}
    return render(request, 'FootballManager/add_team.html', context)


def Add_Match(request):
    if request.method == 'POST':
        form = MatchForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Matches')
    else:
        form = MatchForm()

    context = {'form': form}
    return render(request, 'FootballManager/add_match.html', context)


def Add_to_queue(request, queue_id):
    queue = get_object_or_404(Queue, pk=queue_id)
    matches = Match.objects.all()

    if request.method == 'POST':
        match_ids = request.POST.getlist('matches[]')
        selected_matches = Match.objects.filter(pk__in=match_ids)

        for match in queue.matches.all():
            if match not in selected_matches:
                queue.matches.remove(match)

        for match in selected_matches:
            queue.matches.add(match)

        return redirect('Queue')

    context = {'matches': matches, 'queue': queue}
    return render(request, 'FootballManager/add_to_queue.html', context)


@login_required
def custom_logout(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("Table")


def custom_login(request):
    if request.user.is_authenticated:
        return redirect('Table')

    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                messages.success(request, f"Hello <b>{user.username}</b>! You have been logged in")
                return redirect('Table')

        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    form = AuthenticationForm()

    return render(
        request=request,
        template_name="users/login.html",
        context={'form': form}
    )
