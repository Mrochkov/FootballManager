from django.views import generic
from django.shortcuts import render, get_object_or_404, redirect
from FootballManager.models import Queue, Match

class QueueView(generic.ListView):
    template_name = "FootballManager/queue.html"
    context_object_name = "queues"

    def get_queryset(self):
        return Queue.objects.order_by("id")

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
