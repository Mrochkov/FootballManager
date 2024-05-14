from django.forms import ModelForm
from .models import Footballer
from .models import Team
from .models import Match
from django import forms
from .models import Queue


class FootballerForm(ModelForm):
    class Meta:
        model = Footballer
        fields = '__all__'


class TeamForm(ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'trainer']

class EventForm(ModelForm):
    class Meta:
        model = Queue
        fields = '__all__'

class MatchForm(ModelForm):
    event_form = EventForm()
    class Meta:
        model = Match
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        host_team = cleaned_data.get('host_team')
        guest_team = cleaned_data.get('guest_team')
        if host_team == guest_team:
            raise forms.ValidationError("Drużyna gospodarzy nie może być taka sama jak drużyna gości.")
        return cleaned_data


class QueueForm(ModelForm):
    class Meta:
        model = Queue
        fields = '__all__'
