from django.forms import ModelForm
from .models import Footballer

class FootballerForm(ModelForm):
    class Meta:
        model = Footballer
        fields = '__all__'