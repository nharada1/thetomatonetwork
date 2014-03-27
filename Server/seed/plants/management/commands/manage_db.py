import numpy as np
import plants.models
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'manages db by initing. Usage is ./manage.py manage_db init'
    args = '<management command>'

    def handle(self, *args, **options):
        for command in args:
            if command == 'init':
                self.init_db()

    def init_db(self):
        n = 4
        T = 20
        tau = 1
        L = 0.01
        water_cycle_gradient = 0.042
        water_cycle_mean = 0.5
        init_nutrients = np.array([water_cycle_mean-1.5*water_cycle_gradient,
                                water_cycle_mean-0.5*water_cycle_gradient,
                                water_cycle_mean+.5*water_cycle_gradient,
                                water_cycle_mean+1.5*water_cycle_gradient])
        # Delete everything in DB
        plants.models.PlantState.objects.all().delete()
        plants.models.Plant.objects.all().delete()
        plants.models.AlgoMetadata.objects.all().delete()
        # Create test plants
        new_ivies = []
        for i in range(0,n):
            new_ivies.append(plants.models.EnglishIvy(is_control=False,user_name='user'+str(i),plant_name='plant'+str(i)))
            new_ivies[i].save()
        # Create control plant
        control_ivy = plants.models.EnglishIvy(is_control=True,user_name='control',plant_name='control')
        control_ivy.save()
        # Create initial plant states
        for i in range(0,n):
            new_plant_state = plants.models.PlantState(timestep=0,nutrient_value=init_nutrients[i],plant=new_ivies[i])
            new_plant_state.save()
        # Initialize algo metadata
        new_algometadata = plants.models.AlgoMetadata(L=L,T=T,tau=tau)
        new_algometadata.save()