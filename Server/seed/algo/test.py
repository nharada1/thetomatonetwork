import unclusteredstochasticgd
import numpy as np 
import math

# Testing harness for algorithm
# Emulate MATLAB simulation with hardcoded initial conditions and compoare output

def gaussian(x, mu, sig):
    return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))

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
	P[:,t] = P_t.T
	P_tau = P[:,max(t-tau,0):t+1]
	g,N_t = unclusteredstochasticgd.calcNutrientUpdate(N_tau,P_tau,L,T)
	L = abs(g) if abs(g) > L else L
	N[:,t] = N_t.T
	print(P_t)