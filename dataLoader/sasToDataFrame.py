import pyreadstat
from dataLoader import sasWithChunks

def sasToDataFrame(sasFile, chunkSize=100000):
    convDict = sasWithChunks(sasFile, chunkSize)
    df, meta = pyreadstat.read_sas7bdat(sasFile)
    
    for col, dtype in convDict.items():
        df[col] = df[col].astype(dtype)

    return df