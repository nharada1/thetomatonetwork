import unclusteredstochasticgd
import plants.models
import django.db.models
import numpy as np

# Definitions for variables used in descriptions
# n = number of plant systems
# t = number of time steps since start
# tau = number of time steps in the past to incorporate in gradient estimation
#		(tau=1 => use only current nutrients/performance N[:,t-1] and P[:,t-1])
# N = n x t array of all recorded nutrient dosages (lives in database)
# N_tau = N truncated to only the last tau columns.
# N_t = N[:,t] = new column of N obtained by the algorithm
# P = n x t array of all recorded performance values (lives in database)
# P_tau = P truncated to only the last tau columns. 
# P_t = P[:,t] = new column of P obtained by performance measurement

class DataWrapper:
	def __init__(self):
		self.L = None
		self.T = None
		self.tau = None
		self.t = None
		self.n = None
		self.N_tau = None
		self.P_tau = None
		self.N_t = None
		self.P_t = None
		self.loaded = False
		self.plantIndexMap = {}

	# Load P_tau, N_tau, n, t, tau, L and T from database
	def loadFromDB_nutrientUpdate(self):
		self.L = plants.models.AlgoMetadata.objects.latest('date').L
		self.T = plants.models.AlgoMetadata.objects.latest('date').T
		self.tau = plants.models.AlgoMetadata.objects.latest('date').tau
		self.t = plants.models.PlantState.objects.latest('timestep').timestep
		recent_plant_states = plants.models.PlantState.objects.filter(timestep__gte=self.t-self.tau+1).order_by('timestep','plant')
		self.n = recent_plant_states.aggregate(django.db.models.Count('plant',distinct=True))['plant__count']
		self.N_tau = np.zeros((self.n,self.tau))
		self.P_tau = np.zeros((self.n,self.tau))
		self.P_t = np.zeros((self.n,1))
		for s in range(0,self.tau):
			for i in range(0,self.n):
				self.N_tau[i,s] = recent_plant_states[self.n*s+i].nutrient_value
				self.P_tau[i,s] = recent_plant_states[self.n*s+i].performance_value
				if(self.P_tau[i,s]==0.0):
					return False
				self.plantIndexMap[i] = recent_plant_states[self.n*s+i].plant
		return True

	def loadFromDB_performanceUpdate(self):
		self.L = plants.models.AlgoMetadata.objects.latest('date').L
		self.T = plants.models.AlgoMetadata.objects.latest('date').T
		self.tau = plants.models.AlgoMetadata.objects.latest('date').tau
		self.t = plants.models.PlantState.objects.latest('timestep').timestep
		recent_plant_states = plants.models.PlantState.objects.filter(timestep=self.t).order_by('plant')
		self.n = recent_plant_states.aggregate(django.db.models.Count('plant',distinct=True))['plant__count']
		self.P_t = np.zeros((self.n,1))
		self.N_t = np.zeros((self.n,1))
		for i in range(0,self.n):
			self.N_t[i] = recent_plant_states[i].nutrient_value
			self.P_t[i] = recent_plant_states[i].performance_value
			self.plantIndexMap[i] = recent_plant_states[i].plant

	# Save N_t and L to database
	def persistToDB_nutrientUpdate(self):
		if self.N_t is None:
			self.error('Attempted to persist to db without calculating nutrient update')
		else:
			for i in range(0,self.n):
				plant = self.plantIndexMap[i]
				new_plant_state = plants.models.PlantState(timestep=self.t+1,nutrient_value=self.N_t[i],plant=plant)
				new_plant_state.save()
			new_algometadata = plants.models.AlgoMetadata(L=self.L,T=self.T,tau=self.tau)
			new_algometadata.save()

	def persistToDB_performanceUpdate(self):
		if self.P_t is None:
			self.error('Attempted to persist to db without calculating health update')
		else:
			plant_states_to_update = plants.models.PlantState.objects.filter(timestep=self.t)
			for i in range(0,self.n):
				plant_state_to_update = plant_states_to_update.filter(plant=self.plantIndexMap[i])[0]
				plant_state_to_update.performance_value = self.P_t[i]
				plant_state_to_update.save()

	def calcLipschitz(self):
		pass

	def updateLipschitz(self,g):
		self.L = abs(g) if abs(g) > self.L else self.L

	# A is the algorithm used to update nutrients. For now this is always unclustered gradient descent
	def updateNutrients(self,A=unclusteredstochasticgd.calcNutrientUpdate):
		if self.N_tau is None or self.P_tau is None:
			self.error('Attempted to update nutrients before pulling from database')
		else:
			g,self.N_t = A(self.N_tau,self.P_tau,self.L,self.T)
			self.updateLipschitz(g)

	def updatePerformance(self,plant,p):
		# self.P_t = calculate performance
		if self.P_t is None:
			self.error('Attempted to update nutrients before pulling from database')
		else:
			index = self.plantIndexMap.keys()[self.plantIndexMap.values().index(plant)]
			self.P_t[index] = p

	# Placeholder performance calculator 
	def updatePerformance_test(self,f):
		self.P_t = np.zeros((self.n,))
		print('t: '+str(self.t))
		print('n: '+str(self.n))
		print('N_tau'+str(self.N_tau))
		for i in range(0,self.n):
			self.P_t[i] = f(self.N_tau[i,self.tau-1])

	def error(self,msg):
		print(msg)

	def updateString(self):
		result = []
		for i in range(0,self.n):
			s = str(self.plantIndexMap[i].plant_name + ": " + str(self.N_t[i]))
			result.append(s)
		return result
