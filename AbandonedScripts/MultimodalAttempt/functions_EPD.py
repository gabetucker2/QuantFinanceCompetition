# import scripts
import parameters as P
import functions as F
import statsmodels.api as sm

# functions
def diff(chunk):
    
    daTarget_t, daOpen_t, clOpen_t, innerChunk = F.unpackChunkOuter(chunk)

    da_opens = []
    cl_opens = []
    da_changes = []
    cl_changes = []
    
    for n in range(P.N):
        daTarget_tn, daOpen_tn, clOpen_tn, clHigh_tn, clLow_tn, clClose_tn, clAdjClose_tn, clVolume_tn = F.unpackChunkInner(innerChunk[n])
        da_opens.append(daOpen_tn)
        cl_opens.append(clOpen_tn)
        da_changes.append(daOpen_tn - da_opens[-1])
        cl_changes.append(clOpen_tn - cl_opens[-1])
    
    return da_changes, cl_changes      

def pct_diff_test(chunk):
    daTarget_t, daOpen_t, clOpen_t, innerChunk = F.unpackChunkOuter(chunk)
    
    delta_pct_diff = (daOpen_t - chunk["inputs"][1][1])/chunk["inputs"][1][1]
    oil_pct_diff = (clOpen_t - chunk["inputs"][1][2])/chunk["inputs"][1][2]
    if delta_pct_diff < -0.03:
        print("sell delta stock")
    else:
        pass
    if oil_pct_diff < -0.03:
        print("sell oil")
    else:
        pass