from django import forms
from .models import Simulation, Cashier, ArrivalRate


class SimulationForm(forms.ModelForm):
    class Meta:
        model = Simulation
        fields = '__all__'


class CashierForm(forms.ModelForm):
    class Meta:
        model = Cashier
        fields = '__all__'


class ArrivalRateForm(forms.ModelForm):
    class Meta:
        model = ArrivalRate
        fields = '__all__'
