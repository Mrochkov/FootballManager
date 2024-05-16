from django.views import generic
from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from FootballManager.models import Match, Queue, Statistic
from FootballManager.forms import MatchForm, MatchResultForm

class MatchesView(generic.ListView):
    template_name = "FootballManager/matches.html"
    context_object_name = "matches"

    def get_queryset(self):
        return Match.objects.order_by("-host_team")

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
        matchresult_form = MatchResultForm(request.POST, instance=match)
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
        matchresult_form = MatchResultForm(instance=match)

    context = {'match': match, 'matchresult_form': matchresult_form}
    return render(request, 'FootballManager/add_match_result.html', context)


def Delete_Match(match_id):
    match = get_object_or_404(Match, pk=match_id)
    match.delete()
    return redirect('Matches')

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
