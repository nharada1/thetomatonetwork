import unclusteredstochasticgd

# Definitions for variables used in descriptions
# n = number of plant systems
# t = number of time steps since start
# tau = number of time steps in the past to incorporate in gradient estimation
#		(tau=1 => use only current nutrients/performance N[:,t-1] and P[:,t])
# N = n x t array of all recorded nutrient dosages (lives in database)
# N_tau = N truncated to only the last tau columns.
# N_t = N[:,t] = new column of N obtained by the algorithm
# P = n x (t+1) array of all recorded performance values (lives in database)
# P_tau = P truncated to only the last tau columns. 
# P_t = P[:,t] = new column of P obtained by performance measurement

class DataWrapper:
	def __init__(self,L=0.01,T=20,tau=1):
		self.L = L
		self.T = T
		self.tau = 1

	# Load N_tau amd P_tau from database
	def loadFromDB(self):

	# Save N_t and P_t to database
	def persistToDB(self):

	def calcLipschitz(self):

	def updateLipschitz(g):
		self.L = self.L if abs(g) <= self.L else abs(g)

	def updateNutrients(A=unclusteredstochasticgd.calcNutrientUpdate):
		self.N_t = A(N_tau,P_tau,L,T)

	def updatePerformance():
		# self.P_t = calculate performance

