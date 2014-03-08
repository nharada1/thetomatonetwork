import numpy as np 
import math

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
# P_t = P[:,t] = new column of P obtained by performance measurement (assumed to already be calculated here)

# Return N_t = list of n new nutrient dosages based on past nutrient dosages and performance values
# input: N_tau = n x tau array of nutrient dosages
#        P_tau = n x (tau+1) array of performance values
#		 L = lipschitz constant of performance function 
#		 T = time horizon (value of t when algorithm is expected to converge)

# Notes: "current" nutrient information is at time t-1
#		the performance determined by N[:,t-1] (N_tau[:,tau-1]) is at P[:,t] (P_tau[:,tau])
#		algorithm finds the updates N[:,t] 

# output: Return tuple (g,N_t) 

# Algorithm: Unclustered Stochastic Gradient Descent with Memory
# 1) eta <- L/sqrt(T)
# 2) [I,S] <- all pairs (i,s) such that s=tau-1 (current information) OR 
#					min(N_tau[:,tau-1]) <= N[i,s] <= max(N[:,tau-1]) (recent past information where nutrients 
#														   is between min and max of current nutrient dosages)
# 3) g <- slope of linear regression on locus (N[i,s],P[i,s+1]) := (N_regress,P_regress)
# 4) N_t = N_tau[:,tau-1] + eta*m
# Done

def calcNutrientUpdate(N_tau,P_tau,L,T):
	# Learning rate
	eta = L/math.sqrt(T)
	n,tau = np.shape(N_tau)
	N_regress = np.zeros((n*tau,))
	P_regress = np.zeros((n*tau,))
	minN = 1
	maxN = 0
	i_regress = 0
	for i in range(0,n):
		maxN = N_tau[i,tau-1] if N_tau[i,tau-1] > maxN else maxN
		minN = N_tau[i,tau-1] if N_tau[i,tau-1] < minN else minN
		N_regress[i_regress] = N_tau[i,tau-1]
		P_regress[i_regress] = P_tau[i,tau]
		i_regress = i_regress + 1

	for i in range(0,n):
		for s in range(0,tau-1):
			if minN <= N_tau[i,s] and maxN >= N_tau[i,s]:
				N_regress[i_regress] = N_tau[i,s]
				P_regress[i_regress] = P_tau[i,s+1]
				i_regress = i_regress + 1
	print(i_regress)
	# http://docs.scipy.org/doc/numpy/reference/generated/numpy.linalg.lstsq.html#numpy.linalg.lstsq
	A = np.vstack([N_regress[:i_regress], np.ones(len(N_regress[:i_regress]))]).T
	g, c = np.linalg.lstsq(A, P_regress[:i_regress])[0]

	N_t = N_tau[:,tau-1] + eta*g
	return g,N_t