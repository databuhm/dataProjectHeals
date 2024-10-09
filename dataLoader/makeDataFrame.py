def makeCsvDataFrame(csvFile, encodingDict=None):
    import pandas as pd
    from dataLoader import dataLoaderConfig
    from dataLoader.makeConverters import csvWithChunks
    import os

    fileName = os.path.basename(csvFile)
    
    if encodingDict and fileName in encodingDict:
        encoding = encodingDict[fileName]
    else:
        encoding = dataLoaderConfig.getEncoding()
    
    if encoding is None:
        raise ValueError(f"Encoding is not set for file: {csvFile}")
    
    convDict = csvWithChunks(csvFile)
    df = pd.read_csv(csvFile, converters=convDict, encoding=encoding)
    
    return df

def makeVariousCsvDataFrame(csvDirPath, encodingDict=None) -> dict:
    import os
    from dataLoader.makeDataFrame import makeCsvDataFrame

    if encodingDict is None:
        print("Warning: Encoding dictionary is not provided. Using default 'iso-8859-1' for all files.")
        encodingDict = {file: 'iso-8859-1' for file in os.listdir(csvDirPath) if file.endswith('.csv')}

    dfDict = {}
    csvList = sorted([file for file in os.listdir(csvDirPath) if file.endswith('.csv')])

    for index, csvFile in enumerate(csvList):
        print("Target:", csvFile)
        dfName = f"{os.path.splitext(csvFile)[0].split('_')[0]}_{index}"
        
        csvFilePath = os.path.join(csvDirPath, csvFile)

        df = makeCsvDataFrame(csvFilePath, encodingDict=encodingDict)
        
        dfDict[dfName] = df
        print(f"Result: DataFrame {dfName} with shape {df.shape} and encoding {encodingDict[csvFile]}")
        print("-")

    return dfDict

def makeSasDataFrame(sasFile, chunkSize=100000):
    import pyreadstat
    from dataLoader import dataLoaderConfig
    from dataLoader.makeConverters import sasWithChunks
    
    convDict = sasWithChunks(sasFile, chunkSize)
    df, meta = pyreadstat.read_sas7bdat(sasFile)
    
    encoding = dataLoaderConfig.getEncoding()
    
    for col, dtype in convDict.items():
        df[col] = df[col].astype(dtype)

    return df

def makeVariousSasDataFrame(sasDirPath) -> dict: 
    import os
    from dataLoader.makeDataFrame import makeSasDataFrame
    
    dfDict = {}
    sasList = sorted([file for file in os.listdir(sasDirPath) if file.endswith('.sas7bdat')])
    
    for idx, sasFile in enumerate(sasList):
        print("Target:", idx)
        dfName = f"{os.path.splitext(sasFile)[0]}_{idx}"
        
        sasFilePath = os.path.join(sasDirPath, sasFile)
        df = makeSasDataFrame(sasFilePath)
        
        dfDict[dfName] = df
        print(f"Result: DataFrame {dfName} with shape {df.shape}")
        print("-")

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
