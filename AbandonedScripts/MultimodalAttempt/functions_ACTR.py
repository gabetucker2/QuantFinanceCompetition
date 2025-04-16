# import library
import pyactup

# import scripts
import parameters as P
import functions as F

# functions

def trainMLRLoop(chunk):

    dlTarget_t, dlOpen_t, clOpen_t, innerChunkn = F.unpackChunkOuter(chunk)
    X_train = [dlOpen_t, clOpen_t]
    for n in range(P.N):
        dlTarget_tn, dlOpen_tn, clOpen_tn, clHigh_tn, clLow_tn, clClose_tn, clAdjClose_tn, clVolume_tn = F.unpackChunkInner(innerChunkn[n])
        X_train.extend([dlTarget_tn, dlOpen_tn, clOpen_tn, clHigh_tn, clLow_tn, clClose_tn, clAdjClose_tn, clVolume_tn])

    # working memory

def trainMLRFinal(numChunks):
    
    # average the coefficients across each chunk MLR was ran on

    for i in range(len(P.workingMemory)):
        P.workingMemory[i] /= numChunks
    
    numChunks = 0

def testMLR(chunk):

    dlTarget_t, dlOpen_t, clOpen_t, innerChunkn = F.unpackChunkOuter(chunk)
    X_train = [dlOpen_t, clOpen_t]
    for n in range(P.N):
        dlTarget_tn, dlOpen_tn, clOpen_tn, clHigh_tn, clLow_tn, clClose_tn, clAdjClose_tn, clVolume_tn = F.unpackChunkInner(innerChunkn[n])
        X_train.extend([dlTarget_tn, dlOpen_tn, clOpen_tn, clHigh_tn, clLow_tn, clClose_tn, clAdjClose_tn, clVolume_tn])

    actualValue = dlTarget_t

    predictedValue = P.workingMemory[0]
    # dot product to calculate predicted value
    for i in range(1, len(P.workingMemory)):
        predictedValue += P.workingMemory[i] * X_train[i] # keep in mind X_train is 1D here but 2D in the actual training model

    error = actualValue - predictedValue

    return error
