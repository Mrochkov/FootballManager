from django.forms import ModelForm
from .models import Footballer
from .models import Team


class FootballerForm(ModelForm):
    class Meta:
        model = Footballer
        fields = '__all__'


class TeamForm(ModelForm):
    class Meta:
        model = Team
        fields = '__all__'