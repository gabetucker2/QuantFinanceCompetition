# script imports
import parameters as P

# library imports
import csv
import random

# helper functions

def tryPrintBreak():
    if not P.debuggingMode:
        print("---------------")

def tryPrint(output):
    if not P.debuggingMode:
        print(output)

# math functions

def LERP(start, end, t):
    return (1 - t) * start + t * end

def transpose2D(matrix):
    return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))] # transpose2D

# data functions

def decodeCSV(filePath):
    with open(filePath, newline='') as csvfile:
        # Read the CSV file
        reader = csv.reader(csvfile)
        
        # Extract the rows
        rows = list(reader)
        
        # Check if there are at least two rows
        if len(rows) < 2:
            raise ValueError("CSV file must have at least two rows")
        
        # First row for keys, second row for values
        fields = rows[0][1:] # exclude first column (date)
        values = []
        for row in rows[1:]:
            values.append([float(value) for value in row[1:]])

        return fields, values

def combineChunks(fieldNames, clData, daData):

    outerChunks = []

    T = len(clData) # total number of timesteps
    
    for t in range(P.N, T):

        # create outer chunk

        outerChunk = {
            "inputs" : [
                [daData[t][1], clData[t][1]]
            ],
            "target" : daData[t][fieldNames.index(P.daTargetName)]
        }

        # create inner chunk

        innerChunks = []

        for n in range(1, P.N+1): # n-back

            tn = t - n

            newList = []

            newList.append(daData[tn][fieldNames.index(P.daTargetName)]) # da_target
            newList.append(daData[tn][0])                              # da_open (date is popped)

            newList.append(clData[tn][0])                              # cl_open
            newList.append(clData[tn][1])                              # cl_high
            newList.append(clData[tn][2])                              # cl_low
            newList.append(clData[tn][3])                              # cl_close
            newList.append(clData[tn][4])                              # cl_adjclose
            newList.append(clData[tn][5])                              # cl_vol

            innerChunks.append(newList)
        
        outerChunk["inputs"].extend(innerChunks)

        outerChunks.append(outerChunk)
    
    return outerChunks

def splitChunks(combinedChunks):
    
    rand_ui = random.random()

    totalLength = len(combinedChunks)
    testLength = int(totalLength * (1 - P.ratioTrainTest))

    r = int(LERP(0, totalLength - testLength, rand_ui))
    R = r + testLength

    trainChunks = combinedChunks[P.N:r] + combinedChunks[R+P.N:]
    testChunks = combinedChunks[r+P.N:R]

    return trainChunks, testChunks

# unpackChunkOuter(chunk) -> daTarget_t, daOpen_t, clOpen_t, innerChunk
def unpackChunkOuter(chunk):

    # daTarget_t, daOpen_t, clOpen_t, innerChunk
    return chunk["target"], chunk["inputs"][0][0], chunk["inputs"][0][1], chunk["inputs"][1:]

# unpackChunkInner(innerChunkn) -> daTarget_tn, daOpen_tn, clOpen_tn, clHigh_tn, clLow_tn, clClose_tn, clAdjClose_tn, clVolume_tn
def unpackChunkInner(innerChunkn):
    
    # daTarget_tn, daOpen_tn, clOpen_tn, clHigh_tn, clLow_tn, clClose_tn, clAdjClose_tn, clVolume_tn
    return innerChunkn[0], innerChunkn[1], innerChunkn[2], innerChunkn[3], innerChunkn[4], innerChunkn[5], innerChunkn[6], innerChunkn[7]
