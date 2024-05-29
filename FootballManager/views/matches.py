from django.views import generic
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.forms import modelformset_factory
from FootballManager.models import Match, Team, Footballer, Event, Queue
from FootballManager.forms import MatchForm, MatchResultForm, EventForm

class MatchesView(generic.ListView):
    template_name = "FootballManager/matches/matches.html"
    context_object_name = "matches"

    def get_queryset(self):
        return Match.objects.order_by("-host_team")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        print(timezone.now())
        return context

def Add_Match(request):
    if request.method == 'POST':
        match_form = MatchForm(request.POST)
        if match_form.is_valid():
            match_form.save()
            return redirect('Matches')
    else:
        match_form = MatchForm()

    context = {'match_form': match_form}
    return render(request, 'FootballManager/matches/add_match.html', context)


def Add_Match_Result(request, match_id):
    match = get_object_or_404(Match, pk=match_id)
    EventFormSet = modelformset_factory(Event, form=EventForm, extra=0, can_delete=True)

    host_players = Footballer.objects.filter(team=match.host_team)
    guest_players = Footballer.objects.filter(team=match.guest_team)
    footballers = host_players.union(guest_players)

    if request.method == 'POST':
        matchresult_form = MatchResultForm(request.POST, instance=match)
        formset = EventFormSet(request.POST, queryset=Event.objects.filter(match=match))

        if matchresult_form.is_valid() and formset.is_valid():
            matchresult = matchresult_form.save(commit=False)
            matchresult.host_goals = matchresult_form.cleaned_data['host_goals']
            matchresult.guest_goals = matchresult_form.cleaned_data['guest_goals']
            matchresult.save()

            events = formset.save(commit=False)
            for event in events:
                event.match = match
                event.save()

            for form in formset.deleted_forms:
                form.instance.delete()

            return redirect('Matches')
        else:
            print("MatchResultForm errors:", matchresult_form.errors)
            print("Formset errors:", formset.errors)
    else:
        matchresult_form = MatchResultForm(instance=match)
        formset = EventFormSet(queryset=Event.objects.filter(match=match))

    context = {
        'match': match,
        'matchresult_form': matchresult_form,
        'formset': formset,
        'footballers': footballers,
    }
    return render(request, 'FootballManager/matches/add_match_result.html', context)



def Info_Match(request, match_id):
    match = get_object_or_404(Match, pk=match_id)
    context = {'match': match}
    return render(request, 'FootballManager/matches/info_match.html', context)

def Edit_Match(request, match_id):
    match = get_object_or_404(Match, pk=match_id)

    if request.method == 'POST':
        form = MatchForm(request.POST, instance=match)
        if form.is_valid():
            form.save()
            return redirect('Matches')
    else:
        form = MatchForm(instance=match)

    teams = Team.objects.all()
    queues = Queue.objects.all()

    context = {'form': form, 'match': match, 'teams': teams, 'queues': queues}
    return render(request, 'FootballManager/matches/edit_match.html', context)


def Delete_Match(request, match_id):
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
