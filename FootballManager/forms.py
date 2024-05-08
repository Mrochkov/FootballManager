from django.forms import ModelForm
from .models import Footballer
from .models import Team
from .models import Match
from django import forms

class FootballerForm(ModelForm):
    class Meta:
        model = Footballer
        fields = '__all__'


class TeamForm(ModelForm):
    class Meta:
        model = Team
        fields = '__all__'


class MatchForm(ModelForm):
    class Meta:
        model = Match
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        host_team = cleaned_data.get('host_team')
        guest_team = cleaned_data.get('guest_team')
        if host_team == guest_team:
            raise forms.ValidationError("Host team and guest team cannot be the same.")
        return cleaned_data