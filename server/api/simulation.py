from rest_framework import serializers, viewsets
from simulation.models import SimulationResult
from rest_framework import views

class SimulationResultSerializer(serializers.ModelSerializer):

    class Meta:
        model = SimulationResult
        fields = ['id',
                  'avg_wt',
                  'avg_tis',
                  'rut'
                  ]


class SimulationResultView(viewsets.ModelViewSet):
    queryset = SimulationResult.objects.all()
    serializer_class = SimulationResultSerializer
