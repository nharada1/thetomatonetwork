import unclusteredstochasticgd
from plants.models import Plant, PlantState, AlgoMetadata
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
	def __init__(self,T=20,L=0.01,tau=1):
		self.L = L
		self.T = T
		self.tau = tau
		self.t = None
		self.n = None
		self.N_tau = None
		self.P_tau = None
		self.N_t = None
		self.P_t = None
		self.plantIndexMap = {}

	# Load N_tau, P_tau, L and T from database
	def loadFromDB(self):
		# Load N_tau and P_tau
		self.t = PlantState.objects.all()[-1].timestep
		recent_plant_states = PlantState.objects.filter(timestep__gte=t-self.tau)
		self.n = recent_plant_states.aggregate(Count('plant',True))
		recent_P_and_N = recent_plant_states.order_by('timestep','plant').values('nutrient_value','health_rating','plant')
		self.N_tau = np.zeros((n,tau))
		self.P_tau = np.zeros((n,tau))
		for s in range(0,tau):
			for i in range(0,n):
				self.N_tau[i,s] = recent_P_and_N[n*s+i]['nutrient_value']
				self.P_tau[i,s] = recent_P_and_N[n*s+i]['health_rating']
				self.plantIndexMap[i] = recent_P_and_N[n*s+i]['plant']

		# Load L and T
		self.L = AlgoMetadata.objects.all()[-1].values()['L']
		self.T = AlgoMetadata.objects.all()[-1].values()['T']

	# Save N_t, P_t and L to database
	def persistToDB(self):
		if N_t is None or P_t is None:
			error('Attempted to persist to db without calculating nutrient update')
		else:
			for i in range(0,self.n):
				new_plant_state = PlantState(timestep=self.t+1,nutrient_value=self.N_t[i],health_rating=0.0,plant=self.plantIndexMap[i])
				new_plant_state.save()
			new_algometadata = AlgoMetadata(L=self.L,T=self.T)
			new_algometadata.save()

	def calcLipschitz(self):

	def updateLipschitz(g):
		self.L = self.L if abs(g) <= self.L else abs(g)

	# A is the algorithm used to update nutrients. For now this is always unclustered gradient descent
	def updateNutrients(self,A=unclusteredstochasticgd.calcNutrientUpdate):
		if self.N_tau is None or self.P_tau is None:
			error('Attempted to update nutrients before pulling from database')
		else:
			g,self.N_t = A(self.self.N_tau,P_tau,self.L,self.T)
			updateLipschitz(g)

	def updatePerformance():
		# self.P_t = calculate performance

	def error(msg):
		print(msg)

