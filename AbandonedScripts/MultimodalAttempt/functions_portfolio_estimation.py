import numpy as np
from scipy.optimize import minimize
import functions as F

def BlackScholes(S0, r, sigma, t):
    return S0*np.exp((r-(sigma**2)/2)*t + sigma*np.random.normal(0, t))

def MinusPortolioEV(chunk, x0, a1, a2):
    daTarget_t, daOpen_t, clOpen_t, innerChunk = F.unpackChunkOuter(chunk)
    daTarget_t1, daOpen_t1, clOpen_t1, clHigh_t1, clLow_t1, clClose_t1, clAdjClose_t1, clVolume_t1 = F.unpackChunkInner(innerChunk[1])
    S0 = daOpen_t1
    C0 = clOpen_t1
    r = np.log(1.0527) #change this to real r, or alpha???
    sigma = 0.1 #more on this later
    t = 1/252
    return -(x0 - a1*S0 - a2*C0)*np.epx(r*t) - a1*BlackScholes(S0, r, sigma, t) - a2*BlackScholes(C0, r, sigma, t)

def InitialMinimizationFunction(a1, a2, *args):
    chunk = args[0]
    x0 = args[1]
    S = MinusPortolioEV(chunk, x0, a1, a2)
    return S

chunk_list = []
port_values = []

S = 10,000
for i in chunk_list:
    daTarget_t, daOpen_t, clOpen_t, innerChunk = F.unpackChunkOuter(i)
    daTarget_t1, daOpen_t1, clOpen_t1, clHigh_t1, clLow_t1, clClose_t1, clAdjClose_t1, clVolume_t1 = F.unpackChunkInner(innerChunk[1])
    initial_guess = [0,0]
    result = minimize(InitialMinimizationFunction, initial_guess, args=(i,S))
    coef = result.x
    a1 = coef[0]
    a2 = coef[1]
    S0 = daOpen_t1
    C0 = clOpen_t1
    S1 = daOpen_t
    C1 = clOpen_t
    r = np.log(1.0527)
    sigma = 0.1
    t = 1/252
    PV = (S - a1*S0 - a2*C0)*np.epx(r*t) - a1*S1 - a2*C1
    port_values.append(PV)
