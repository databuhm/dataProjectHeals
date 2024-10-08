def makeCsvDataFrame(csvFile):
    import pandas as pd
    from dataLoader.legacyMakeConverters import csvWithChunks
    
    convDict = csvWithChunks(csvFile)
    df = pd.read_csv(csvFile, converters=convDict)
    
    return df

def makeSasDataFrame(sasFile, chunkSize=100000):
    import pyreadstat
    from dataLoader.legacyMakeConverters import sasWithChunks
    
    convDict = sasWithChunks(sasFile, chunkSize)
    df, meta = pyreadstat.read_sas7bdat(sasFile)
    
    for col, dtype in convDict.items():
        df[col] = df[col].astype(dtype)

    return df