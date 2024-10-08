def makeCsvDataFrame(csvFile):
    import pandas as pd
    from dataLoader.makeConverters import csvWithChunks
    
    convDict = csvWithChunks(csvFile)
    df = pd.read_csv(csvFile, converters=convDict)
    
    return df

def makeVariousCsvDataFrame(csvDirPath) -> dict:
    import os
    from dataLoader.makeDataFrame import makeCsvDataFrame
    
    dfDict = {}
    csvList = sorted([file for file in os.listdir(csvDirPath) if file.endswith('.csv')])
    
    for index, csvFile in enumerate(csvList):
        dfName = f"{os.path.splitext(csvFile)[0].split('_')[0]}_{index}"
        
        csvFilePath = os.path.join(csvDirPath, csvFile)
        df = makeCsvDataFrame(csvFilePath)
        
        dfDict[dfName] = df
        print(f"make {dfName} is Ready: {df.shape}")

    return dfDict

def makeSasDataFrame(sasFile, chunkSize=100000):
    import pyreadstat
    from dataLoader.makeConverters import sasWithChunks
    
    convDict = sasWithChunks(sasFile, chunkSize)
    df, meta = pyreadstat.read_sas7bdat(sasFile)
    
    for col, dtype in convDict.items():
        df[col] = df[col].astype(dtype)

    return df

def makeVariousSasDataFrame(sasDirPath) -> dict: 
    import os
    from dataLoader.makeDataFrame import makeSasDataFrame
    
    dfDict = {}
    sasList = sorted([file for file in os.listdir(sasDirPath) if file.endswith('.sas7bdat')])
    
    for idx, sasFile in enumerate(sasList):
        dfName = f"{os.path.splitext(sasFile)[0]}_{idx}"
        
        sasFilePath = os.path.join(sasDirPath, sasFile)
        df = makeSasDataFrame(sasFilePath)
        
        dfDict[dfName] = df
        print(f"make {dfName} is Ready: {df.shape}")

    return dfDict