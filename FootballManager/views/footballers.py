from django.views import generic
from django.shortcuts import render, redirect
from FootballManager.models import Footballer, Statistic
from FootballManager.forms import FootballerForm

class FootballersView(generic.ListView):
    template_name = "FootballManager/footballers.html"
    context_object_name = "footballers"

    def get_queryset(self):
        return Footballer.objects.order_by("-name")

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
