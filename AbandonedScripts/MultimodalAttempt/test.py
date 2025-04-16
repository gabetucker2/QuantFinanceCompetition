# script imports
import functions as F
import parameters as P

# library imports
# TODO: add

# shell
F.tryPrintBreak()
F.tryPrint("TEST START")

######################################################

fields, clData = F.decodeCSV(P.clDataPath)
_, daData = F.decodeCSV(P.daDataPath)

print(fields)

######################################################

# shell
F.tryPrint("TEST STOP")
F.tryPrintBreak()
