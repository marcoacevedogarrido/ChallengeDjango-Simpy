from django.db import models


class Simulation(models.Model):
    n_prod_min = models.IntegerField()
    n_prod_max = models.IntegerField()
    proc_time = models.FloatField()
    replica = models.IntegerField()


class Cashier(models.Model):
    start_time = models.IntegerField()
    end_time = models.IntegerField()
    n = models.IntegerField()
    simulation = models.ForeignKey(Simulation, on_delete=models.CASCADE)


class ArrivalRate(models.Model):
    hour = models.IntegerField()
    arrivals = models.IntegerField()
    simulation = models.ForeignKey(Simulation, on_delete=models.CASCADE)


class SimulationResult(models.Model):
    avg_wt = models.FloatField()
    avg_tis = models.FloatField()
    simulation = models.ForeignKey(Simulation, on_delete=models.CASCADE)
