def makeCsvDataFrame(csvFile:str, encodingDict:dict=None):
    
    """
    Creates a DataFrame from a CSV file, applying appropriate encoding and data type conversions.
    
    Args:
        csvFile (str): The path to the CSV file.
        encodingDict (dict): A dictionary of file names and their corresponding encodings.
        
    Returns:
        pd.DataFrame: A pandas DataFrame created from the CSV file.
    """
    
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

def makeMultiCsvDataFrame(csvDirPath:str, encodingDict:dict=None) -> dict:
    
    """
    Creates DataFrames from multiple CSV files in a directory and stores them in a dictionary.
    
    Args:
        csvDirPath (str): The directory containing CSV files.
        encodingDict (dict): A dictionary of file names and their corresponding encodings.
        
    Returns:
        dict: A dictionary with file names (without extensions) as keys and their corresponding DataFrames as values.
    """
    
    import os
    from dataLoader.makeDataFrame import makeCsvDataFrame

    if encodingDict is None:
        print("Warning: Encoding dictionary is not provided. Using default 'iso-8859-1' for all files.")
        encodingDict = {file: 'iso-8859-1' for file in os.listdir(csvDirPath) if file.endswith('.csv')}

    dfDict = {}
    csvList = sorted([file for file in os.listdir(csvDirPath) if file.endswith('.csv')])

    for idx, csvFile in enumerate(csvList):
        print(f"Processing file {idx+1}/{len(csvList)}: {csvFile}")

        dfName = csvFile.split('.')[0]
        csvFilePath = os.path.join(csvDirPath, csvFile)

        try:
            df = makeCsvDataFrame(csvFilePath, encodingDict=encodingDict)

            dfDict[dfName] = df
            print(f"Result: DataFrame {dfName} with shape {df.shape} and encoding {encodingDict[csvFile]}")
            print("-")

        except Exception as e:
            print(f"Failed to process {csvFile}. Error: {e}")

    print(f"Completed processing {len(dfDict)} out of {len(csvList)} files.")

    return dfDict

def makeSasDataFrame(sasFile:str, chunkSize=100000):
    
    """
    Creates a DataFrame from a SAS file, reading the file in chunks.
    
    Args:
        sasFile (str): The path to the SAS file.
        chunkSize (int): The number of rows per chunk. Default is 100,000 rows.
        
    Returns:
        pd.DataFrame: A pandas DataFrame created from the SAS file.
    """

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

def makeMultiSasDataFrame(sasDirPath:str) -> dict: 
    
    """
    Creates DataFrames from multiple SAS files in a directory and stores them in a dictionary.
    
    Args:
        sasDirPath (str): The directory containing SAS files.
        
    Returns:
        dict: A dictionary with file names (without extensions) as keys and their corresponding DataFrames as values.
    """
    
    import os
    from dataLoader.makeDataFrame import makeSasDataFrame
    
    dfDict = {}
    sasList = sorted([file for file in os.listdir(sasDirPath) if file.endswith('.sas7bdat')])
    
    for idx, sasFile in enumerate(sasList):
        print(f"Processing file {idx+1}/{len(sasList)}: {sasFile}")
        
        sasFilePath = os.path.join(sasDirPath, sasFile)
        
        try:
            df = makeSasDataFrame(sasFilePath)
            dfName = os.path.splitext(sasFile)[0]
            dfDict[dfName] = df
            print(f"Result: DataFrame {dfName} with shape {df.shape}")
        
        except Exception as e:
            print(f"Failed to process {sasFile}. Error: {e}")
        
        print("-")
    print(f"Completed processing {len(dfDict)} out of {len(sasList)} files.")

    return dfDict

def makeOneDataFrame(dfDict:dict):
    
    """
    Combines multiple DataFrames into one DataFrame by concatenating them along the rows.
    
    Args:
        dfDict (dict): A dictionary with DataFrame names as keys and DataFrames as values.
        
    Returns:
        pd.DataFrame: A combined DataFrame.
    """
    
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

def eachSingleDfToDict(fileNames:list, dataFrameNames:list) -> dict:
    
    """
    Converts individual file names and DataFrame names into a dictionary.
    
    Args:
        fileNames (list): List of file names (with extensions).
        dataFrameNames (list): List of corresponding DataFrame names.
        
    Returns:
        dict: A dictionary with file names (without extensions) as keys and DataFrame names as values.
        
    Raises:
        ValueError: If the lengths of fileNames and dataFrameNames do not match.
    """
    
    import os

    if len(fileNames) != len(dataFrameNames):
        raise ValueError("The length of keys and values must match.")

    dfDict = {os.path.splitext(fileNames[i])[0]: dataFrameNames[i] for i in range(len(fileNames))}
    
    return dfDict