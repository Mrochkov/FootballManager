from django.views import generic
from django.shortcuts import render, redirect, get_object_or_404
from FootballManager.models import Team, Footballer
from FootballManager.forms import TeamForm

class TeamsView(generic.ListView):
    template_name = "FootballManager/teams.html"
    context_object_name = "teams"

    def get_queryset(self):
        return Team.objects.order_by("-name")


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


def Info_Team(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    footballers = Footballer.objects.filter(team=team)
    context = {'team': team, 'footballers': footballers}
    return render(request, 'FootballManager/info_team.html', context)


def Edit_Team(request, team_id):
    team = get_object_or_404(Team, pk=team_id)

    if request.method == 'POST':
        form = TeamForm(request.POST, instance=team)
        if form.is_valid():
            form.save()
            return redirect('Teams')
    else:
        form = TeamForm(instance=team)

    context = {'team': team}
    return render(request, 'FootballManager/edit_team.html', context)


def Delete_Team(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    team.delete()
    return redirect('Teams')

