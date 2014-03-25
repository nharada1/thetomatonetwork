import unclusteredstochasticgd
import numpy as np 
import math
import datawrapper as dw
import plants.models 

# Testing harness for algorithm
# Emulate MATLAB simulation with hardcoded initial conditions and compoare output

def gaussian(x, mu, sig):
    return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))

def testAlgoNoDB():
	n = 4
	T = 20
	tau = 1
	L = 0.01
	N = np.zeros((n,T))
	N[:,0] = np.array([0.3931,0.4580,0.5677,0.4464]).T
	P = np.zeros((n,T+1))
	sig = 0.4505
	mu = 0.7482

	for t in range(1,20):
		N_tau = N[:,max(t-tau,0):t]
		P_t = np.zeros((n,))
		for i in range(0,n):
			P_t[i] = gaussian(N[i,t-1],mu,sig)
		P[:,t-1] = P_t.T
		P_tau = P[:,max(t-tau,0):t]
		g,N_t = unclusteredstochasticgd.calcNutrientUpdate(N_tau,P_tau,L,T)
		L = abs(g) if abs(g) > L else L
		N[:,t] = N_t.T
		print(N_tau)
		print(P_t)
		print(L)

def testAlgoDB():
	initTestDB()
	n = 4
	T = 20
	tau = 1
	L = 0.01
	sig = 0.4505
	mu = 0.7482
	f = lambda x: gaussian(x,mu,sig)
	for t in range(1,T):
		wrapper = dw.DataWrapper()
		wrapper.loadFromDB()
		wrapper.updatePerformance_test(f)
		wrapper.persistToDB_performanceUpdate()
		wrapper.loadFromDB()
		wrapper.updateNutrients()
		wrapper.persistToDB_nutrientUpdate()

def initTestDB():
	n = 4
	T = 20
	tau = 1
	L = 0.01
	init_nutrients = np.array([0.3931,0.4580,0.5677,0.4464])
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