from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import F, Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db import models, transaction

from FootballManager.models import Footballer, Team, Match, Queue, Statistic
from FootballManager.forms import FootballerForm, TeamForm, MatchForm, QueueForm, EventForm, MatchResultForm





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
        return Statistic.objects.select_related('footballer').order_by("-goals_scored")
    

def Add_Footballer(request):
    form = FootballerForm()

    if request.method == 'POST':
        form = FootballerForm(request.POST)
        if form.is_valid():
            footballer = form.save()
            Statistic.objects.create(footballer=footballer)
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


def update_team_statistics(team, goals_scored, goals_lost, is_winner, is_draw):
    if is_winner:
        team.wins += 1
    elif is_draw:
        team.draws += 1
    else:
        team.losses += 1

    team.goals_scored += goals_scored
    team.goals_lost += goals_lost
    team.save()

@transaction.atomic
def update_team_stats_for_match(host_team, guest_team, host_goals, guest_goals):
    if host_goals > guest_goals:
        update_team_statistics(host_team, host_goals, guest_goals, is_winner=True, is_draw=False)
        update_team_statistics(guest_team, guest_goals, host_goals, is_winner=False, is_draw=False)
    elif host_goals < guest_goals:
        update_team_statistics(host_team, host_goals, guest_goals, is_winner=False, is_draw=False)
        update_team_statistics(guest_team, guest_goals, host_goals, is_winner=True, is_draw=False)
    else:
        update_team_statistics(host_team, host_goals, guest_goals, is_winner=False, is_draw=True)
        update_team_statistics(guest_team, guest_goals, host_goals, is_winner=False, is_draw=True)


def Add_Match(request):
    if request.method == 'POST':
        match_form = MatchForm(request.POST)
        if match_form.is_valid():
            match_form.save()
            

            return redirect('Matches')
    else:
        match_form = MatchForm()

    context = {'match_form': match_form}
    return render(request, 'FootballManager/add_match.html', context)

def Add_Match_Result(request, match_id):
    match = get_object_or_404(Match, pk=match_id)
    if request.method == 'POST':
        matchresult_form = MatchResultForm(request.POST)
        if matchresult_form.is_valid():
            matchresult = matchresult_form.save()
            update_team_stats_for_match(
                            match.host_team,
                            match.guest_team,
                            matchresult.host_goals,
                            matchresult.guest_goals
                        )
            return redirect('Matches')
    else:
        matchresult_form = MatchResultForm()

    context = {'match': match, 'matchresult_form': matchresult_form}
    return render(request, 'FootballManager/add_match_result.html', context)


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
