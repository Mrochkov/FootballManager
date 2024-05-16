from django.views import generic
from django.shortcuts import render, redirect
from FootballManager.models import Team
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
