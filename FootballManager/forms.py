from django.forms import ModelForm
from django import forms
from .models import Footballer, Team, Match, Queue, Event


class FootballerForm(ModelForm):
    class Meta:
        model = Footballer
        fields = '__all__'


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'trainer', 'logo', 'description']


class EventForm(ModelForm):
    class Meta:
        model = Queue
        fields = '__all__'


class MatchForm(ModelForm):
    class Meta:
        model = Match
        fields = ['date', 'host_team', 'guest_team', 'queue']

    def clean(self):
        cleaned_data = super().clean()
        host_team = cleaned_data.get('host_team')
        guest_team = cleaned_data.get('guest_team')
        if host_team == guest_team:
            raise forms.ValidationError("Drużyna gospodarzy nie może być taka sama jak drużyna gości.")
        return cleaned_data


class MatchResultForm(ModelForm):
    class Meta:
        model = Match
        fields = ['host_goals', 'guest_goals']


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['minute', 'event_type', 'footballer']


class QueueForm(ModelForm):
    matches = forms.ModelMultipleChoiceField(queryset=Match.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)
    class Meta:
        model = Queue
        fields = ['number', 'matches']
