from django.views import generic
from django.shortcuts import render, redirect, get_object_or_404
from FootballManager.models import Queue
from FootballManager.forms import QueueForm

class QueueView(generic.ListView):
    template_name = "FootballManager/queues/queues.html"
    context_object_name = "queues"

    def get_queryset(self):
        return Queue.objects.order_by("id")

def Add_Queue(request):
    if request.method == 'POST':
        form = QueueForm(request.POST)
        if form.is_valid():
            queue = form.save(commit=False)
            queue.save()
            form.save_m2m()  
            return redirect('Queues')
    else:
        form = QueueForm()
    return render(request, 'FootballManager/queues/add_queue.html', {'form': form})

def Info_Queue(request, queue_id):
    queue = get_object_or_404(Queue, pk=queue_id)
    context = {'queue': queue}
    return render(request, 'FootballManager/queues/info_queue.html', context)


def Edit_Queue(request, queue_id):
    queue = get_object_or_404(Queue, pk=queue_id)

    if request.method == 'POST':
        form = QueueForm(request.POST, instance=queue)
        if form.is_valid():
            form.save()
            return redirect('Queues')
    else:
        form = QueueForm(instance=queue)

    context = {'form': form, 'queue': queue}
    return render(request, 'FootballManager/queues/edit_queue.html', context)


def Delete_Queue(request, queue_id):
    queue = get_object_or_404(Queue, pk=queue_id)
    queue.delete()
    return redirect('Queues')


