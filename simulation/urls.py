from django.urls import path
from . import views
from rest_framework import routers
from server.api.simulation import SimulationResultView

router = routers.SimpleRouter()
router.register(r'result/', SimulationResultView, 'simulationresult')

urlpatterns = [
    path('', views.index, name='index'),
    path('ingresar/', views.simulation, name='simulation'),
    path('graficos/', views.chart, name='chart'),
]
urlpatterns += router.urls
