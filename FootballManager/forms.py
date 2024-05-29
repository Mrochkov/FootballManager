from django.forms import ModelForm
from django import forms
from .models import Footballer, Team, Match, Queue, Event


class FootballerForm(ModelForm):
    class Meta:
        model = Footballer
        fields = '__all__'

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise forms.ValidationError("Pole imienia nie może być puste.")
        return name

    def clean_surname(self):
        surname = self.cleaned_data.get('surname')
        if not surname:
            raise forms.ValidationError("Pole nazwiska nie może być puste.")
        return surname


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'trainer', 'logo', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Wprowadź nazwę drużyny'}),
            'trainer': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Wprowadź imię i nazwisko trenera'}),
            'logo': forms.ClearableFileInput(attrs={'class': 'file-input'}),
            'description': forms.Textarea(attrs={'class': 'textarea', 'placeholder': 'Wprowadź opis drużyny'}),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        instance = getattr(self, 'instance', None)
        if instance and Team.objects.filter(name=name).exclude(pk=instance.pk).exists():
            raise forms.ValidationError("Drużyna o tej nazwie już istnieje.")
        return name

    def clean_trainer(self):
        trainer = self.cleaned_data.get('trainer')
        if not trainer:
            raise forms.ValidationError("Pole trenera nie może być puste.")
        return trainer


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

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if not date:
            raise forms.ValidationError("Data meczu jest wymagana.")
        return date


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
