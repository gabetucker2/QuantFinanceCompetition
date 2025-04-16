# import scripts
import parameters as P
import functions as F

# functions

def trainPolyReg(chunk):

    daTarget_t, daOpen_t, clOpen_t, prevChunks = F.unpackChunkOuter(chunk)
    
    for n in range(P.N):
        daTarget_tn, daOpen_tn, clOpen_tn, clHigh_tn, clLow_tn, clClose_tn, clAdjClose_tn, clVolume_tn = F.unpackChunkInner(prevChunks[n])

        # TODO: Do stuff here updating based on t - 1.  You can do this in the loop for each previous timestep's data, or you can do it all at once outside this loop depending on your algorithm treating all data in "prevChunks", "daOpen_t", and "clOpen_t" as athe training data.

    P.workingMemory = [] # update working memory accordingly along the way

def testPolyReg(chunk):
    print("test")
