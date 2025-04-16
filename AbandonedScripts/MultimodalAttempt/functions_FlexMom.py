# import scripts
import parameters as P
import functions as F

# functions
def trainACTR(chunk):
    
    daTarget_t, daOpen_t, clOpen_t, innerChunk = F.unpackChunkOuter(chunk)

    for n in range(P.N):
        daTarget_tn, daOpen_tn, clOpen_tn, clHigh_tn, clLow_tn, clClose_tn, clAdjClose_tn, clVolume_tn = F.unpackChunkInner(innerChunk[n])
        
    P.workingMemory = [] # update working memory accordingly along the way

def testACTR(daTarget_t, daOpen_t, clOpen_t, prevChunks):
    actualValue = chunk[-1]
    predictedValue = ...

    return actualValue - predictedValue
