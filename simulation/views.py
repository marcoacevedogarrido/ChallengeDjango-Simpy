from django.shortcuts import render
from .models import Cashier, Simulation
from .forms import SimulationForm, CashierForm, ArrivalRateForm
from django.shortcuts import redirect
from django.views.generic import CreateView
from django.db.models import Sum

def index(request):
    cashier = Cashier.objects.all()
    c = {'cashiers':cashier}
    return render(request, 'index.html', c)


def simulation(request):
    if request.method == 'POST':
        formsimulation = SimulationForm(request.POST)
        formcashier =  CashierForm(request.POST)
        formarrival = ArrivalRateForm(request.POST)
        if formsimulation.is_valid() and formcashier.is_valid() and formarrival.is_valid():
            formsimulation.save()
            formcashier.save()
            formarrival.save()
        return redirect('index')
    else:
        formsimulation = SimulationForm()
        formcashier = CashierForm()
        formarrival = ArrivalRateForm()
    return render(request, 'formulario.html', {'formsimulation':formsimulation, 'formcashier':formcashier, 'formarrival':formarrival})


def chart(request):
    labels = []
    data = []

    queryset = Cashier.objects.order_by('-start_time')[:2]
    for cashier in queryset:
        labels.append(cashier.id)
        data.append(cashier.start_time)

    return render(request, 'chart.html', {
        'labels': labels,
        'data': data,
    })
