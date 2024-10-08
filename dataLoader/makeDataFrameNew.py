def makeCsvDataFrame(csvFile):
    import pandas as pd
    from dataLoader import globalConfig
    from dataLoader.makeConvertersNew import csvWithChunks
    
    encoding = globalConfig.getEncoding()
    
    convDict = csvWithChunks(csvFile)
    df = pd.read_csv(csvFile, converters=convDict, encoding=encoding)
    
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
    import pyreadstat, globalConfig
    from dataLoader.makeConvertersNew import sasWithChunks
    from dataLoader import globalConfig
    
    convDict = sasWithChunks(sasFile, chunkSize)
    df, meta = pyreadstat.read_sas7bdat(sasFile)
    
    encoding = globalConfig.getEncoding()
    
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

def makeOneDataFrame(dfDict: dict):
    import pandas as pd
    import datetime, time
    
    print("Start: ", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    start = time.time()
    
    dfList = list(dfDict.values())
    combinedDf = pd.concat(dfList, axis=0, ignore_index=True, sort=False)
    
    print(f"Shape of DataFrame: {combinedDf.shape}")
    print("End: ", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print("Running: ", str(datetime.timedelta(seconds=(time.time() - start))).split(".")[0])
    
    return combinedDf
