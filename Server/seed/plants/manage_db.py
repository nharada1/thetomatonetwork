import unclusteredstochasticgd
import numpy as np 
import math
import datawrapper as dw
import plants.models 

def initDB():
	n = 4
	T = 20
	tau = 1
	L = 0.01
	water_cycle_gradient = 0.042
	water_cycle_mean = 0.5
	init_nutrients = np.array([water_cycle_mean-1.5*water_cycle_gradient
							water_cycle_mean-0.5*water_cycle_gradient,
							water_cycle_mean+.5*water_cycle_gradient,
							water_cycle_mean+1.5*water_cycle_gradient])
	# Delete everything in DB
	plants.models.PlantState.objects.all().delete()
	plants.models.Plant.objects.all().delete()
	plants.models.AlgoMetadata.objects.all().delete()
	# Create plants
	new_ivies = []
	for i in range(0,n):
		new_ivies.append(plants.models.EnglishIvy(user_name='user'+str(i),plant_name='plant'+str(i)))
		new_ivies[i].save()
	# Create initial plant states
	for i in range(0,n):
		new_plant_state = plants.models.PlantState(timestep=0,nutrient_value=init_nutrients[i],plant=new_ivies[i])
		new_plant_state.save()
	# Initialize algo metadata
	new_algometadata = plants.models.AlgoMetadata(L=L,T=T,tau=tau)
	new_algometadata.save()