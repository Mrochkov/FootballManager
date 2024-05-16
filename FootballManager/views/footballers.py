from django.views import generic
from django.shortcuts import render, redirect, get_object_or_404
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

def Info_Footballer(request, footballer_id):
    footballer = get_object_or_404(Footballer, pk=footballer_id)
    context = {'footballer': footballer}
    return render(request, 'FootballManager/info_footballer.html', context)

def Edit_Footballer(request, footballer_id):
    footballer = get_object_or_404(Footballer, pk=footballer_id)

    if request.method == 'POST':
        form = FootballerForm(request.POST, instance=footballer)
        if form.is_valid():
            form.save()
            return redirect('Footballers')
    else:
        form = FootballerForm(instance=footballer)

    context = {'form': form, 'footballer': footballer}
    return render(request, 'FootballManager/edit_footballer.html', context)


def Delete_Footballer(request, footballer_id):
    footballer = get_object_or_404(Footballer, pk=footballer_id)
    footballer.delete()
    return redirect('Footballers')
