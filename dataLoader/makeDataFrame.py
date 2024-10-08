def makeCsvDataFrame(csvFile):
    import pandas as pd
    from dataLoader.makeConverters import csvWithChunks
    
    convDict = csvWithChunks(csvFile)
    df = pd.read_csv(csvFile, converters=convDict)
    
    return df

def makeSasDataFrame(sasFile, chunkSize=100000):
    import pyreadstat
    from dataLoader.makeConverters import sasWithChunks
    
    convDict = sasWithChunks(sasFile, chunkSize)
    df, meta = pyreadstat.read_sas7bdat(sasFile)
    
    for col, dtype in convDict.items():
        df[col] = df[col].astype(dtype)

    return df

def makeVariousSasDataFrame(sasFolderPath) -> dict: 
    import os
    
    dfDict = {}
    sasList = sorted([file for file in os.listdir(sasFolderPath) if file.endswith('.sas7bdat')])
    
    for idx, sasFile in enumerate(sasList):
        dfName = f"{os.path.splitext(sasFile)[0]}_{idx}"
        
        sasFilePath = os.path.join(sasFolderPath, sasFile)
        df = makeSasDataFrame(sasFilePath)
        
        dfDict[dfName] = df
        print(f"make {dfName} is Ready: {df.shape}")

    return dfDict