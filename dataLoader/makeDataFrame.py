def makeCsvDataFrame(csvFile, encodingDict=None):
    import pandas as pd
    import os
    from dataLoader.makeConverters import csvWithChunks

    fileName = os.path.basename(csvFile)

    if encodingDict and fileName in encodingDict:
        encoding = encodingDict[fileName]
    else:
        print(f"Warning: Encoding for '{fileName}' not provided. Using default 'ISO-8859-1'.")
        encoding = 'ISO-8859-1'
    
    convDict = csvWithChunks(csvFile, encodingDict=encodingDict)
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

    for csvFile in csvList:
        print("Target:", csvFile)

        dfName = csvFile.split('.')[0]
        csvFilePath = os.path.join(csvDirPath, csvFile)

        df = makeCsvDataFrame(csvFilePath, encodingDict=encodingDict)

        dfDict[dfName] = df
        print(f"Result: DataFrame {dfName} with shape {df.shape} and encoding {encodingDict[csvFile]}")
        print("-")

    return dfDict

def makeSasDataFrame(sasFile, chunkSize=100000):
    import pyreadstat, os
    from dataLoader.makeConverters import sasWithChunks

    fileName = os.path.basename(sasFile)

    print(f"Reading SAS file '{sasFile}' with default encoding (utf-8 or file metadata).")

    convDict = sasWithChunks(sasFile, chunkSize)
    df, meta = pyreadstat.read_sas7bdat(sasFile)

    for col, dtype in convDict.items():
        df[col] = df[col].astype(dtype)

    print(f"Result: DataFrame {df} with shape {df.shape}.")
    print("-")
    
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

def eachSingleDfToDict(fileNames, dataFrameNames) -> dict:
    import os

    if len(fileNames) != len(dataFrameNames):
        raise ValueError("The length of keys and values must match.")

    dfDict = {os.path.splitext(fileNames[i])[0]: dataFrameNames[i] for i in range(len(fileNames))}
    
    return dfDict