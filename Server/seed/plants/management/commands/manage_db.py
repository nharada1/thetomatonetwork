import numpy as np
import plants.models
from django.core.management.base import BaseCommand
import datetime
from django.db.models import Q


class Command(BaseCommand):
    help = 'manages db by initing. Usage is ./manage.py manage_db init'
    args = '<management command>'
    n = 4
    T = 14
    tau = 1
    L = 0
    water_cycle_gradient = 0.084
    water_cycle_mean = 0.5
    init_nutrients = np.array([water_cycle_mean-1.5*water_cycle_gradient,
                            water_cycle_mean-0.5*water_cycle_gradient,
                            water_cycle_mean+.5*water_cycle_gradient,
                            water_cycle_mean+1.5*water_cycle_gradient])

    def handle(self, *args, **options):
        for command in args:
            if command == 'init':
                self.init_db()
            elif command == 'init_plants':
                self.init_plants()
            elif command == 'reset_plants':
                self.reset_plants()
            elif command == 'init_algo':
                self.init_algo()
            elif command == 'init_care':
                self.init_care()
            elif command=='migrate_control_plants':
                self.migrate_control_plants()
            elif command=='migrate_plants_for_new_experiment':
                self.migrate_plants_for_new_experiment()

    def init_db(self):
        new_ivies,control_ivy = self.init_plants()
        self.init_plantstates(new_ivies,control_ivy)
        self.init_care()
        self.init_algo()

    def init_plants(self):
        plants.models.Plant.objects.all().delete()
         # Create test plants
        new_ivies = []
        for i in range(0,self.n):
            new_ivies.append(plants.models.EnglishIvy(initial_date=datetime.datetime(year=2014,month=3,day=27,hour=20,minute=8),
                                                    is_control=False,user_name='user'+str(i),plant_name='plant'+str(i)))
            new_ivies[i].save()
        # Create control plant
        control_ivy = plants.models.EnglishIvy(initial_date=datetime.datetime(year=2014,month=3,day=27,hour=20,minute=8),
                                            is_control=True,user_name='control',plant_name='control')
        control_ivy.save()
        return new_ivies,control_ivy

    def init_plantstates(self,new_ivies,control_ivy):
        plants.models.PlantState.objects.all().delete()
        # Create initial plant states
        for i in range(0,self.n):
            plant = new_ivies[i]
            new_plant_state = plants.models.PlantState(timestep=0,nutrient_value=self.init_nutrients[i],plant=plant)
            new_plant_state.save()
        control_plant_state = plants.models.PlantState(timestep=0,nutrient_value=0,plant=control_ivy)
        control_plant_state.save()

    def reset_plants(self):
        ivies = plants.models.Plant.objects.all()
        for p in ivies:
            p.initial_date = datetime.datetime(year=2014,month=3,day=27,hour=20,minute=8)
            p.save()

    def init_algo(self):
        plants.models.AlgoMetadata.objects.all().delete()
        new_algometadata = plants.models.AlgoMetadata(L=self.L,T=self.T,tau=self.tau)
        new_algometadata.save()

    def init_care(self):
        plants.models.CareConstants.objects.all().delete()
        care_constants = plants.models.CareConstants(water_cycle_period=7200,light_start_hour=8,light_end_hour=20)
        care_constants.save()

    def migrate_control_plants(self):
        control_plant_states = plants.models.ControlPlantState.objects.all()
        for control_plant_state in control_plant_states:
            plant_state = plants.models.PlantState(date=control_plant_state.date,
                timestep=control_plant_state.timestep,nutrient_value=0.0,plant=control_plant_state.plant,
                performance_value=control_plant_state.performance_value)
            plant_state.save()

    def migrate_plants_for_new_experiment(self):
        # Set is_control on new control plants
        plants_to_become_control = plants.models.Plant.objects.filter(Q(plant_name='plant0') | Q(plant_name='plant3'))
        for plant in plants_to_become_control:
            plant.is_control = True
            plant.save()
        # Set fixed nutrient values for control plants
        t = plants.models.PlantState.objects.latest('date').timestep
        control_plant1 = plants.models.PlantState.objects.filter(timestep=t,plant__plant_name='plant0')[0]
        control_plant1.nutrient_value = 0.125
        control_plant1.save()
        control_plant2 = plants.models.PlantState.objects.filter(timestep=t,plant__plant_name='plant3')[0]
        control_plant2.nutrient_value = 1
        control_plant2.save()
