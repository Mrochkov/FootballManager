from django.views import generic
from FootballManager.models import Statistic

class StatisticView(generic.ListView):
    template_name = "FootballManager/statistics.html"
    context_object_name = "statistics"

    def get_queryset(self):
        return Statistic.objects.select_related('footballer').order_by("-goals_scored")
