def getFileEncoding(filePath, sampleSize=100000000):
    from dataLoader import dataLoaderConfig
    import chardet
    try:
        with open(filePath, 'rb') as file:
            raw_data = file.read(sampleSize)
        
        result = chardet.detect(raw_data)
        detectedEncoding = result['encoding']
        
        if detectedEncoding is None or detectedEncoding.lower() == 'ascii':
            print(f"Detected Encoding: {detectedEncoding}. Changing to 'ISO-8859-1' for use.")
            dataLoaderConfig.setEncoding('ISO-8859-1')
        else:
            print(f"Detected file encoding: {detectedEncoding}")
            dataLoaderConfig.setEncoding(detectedEncoding)
    
    except Exception as e:
        print(f"Error occurred while detecting encoding: {e}. Using default 'ISO-8859-1'.")
        dataLoaderConfig.setEncoding('ISO-8859-1')
    
    return dataLoaderConfig.getEncoding()

def csvWithChunks(csvFile, chunkSize=100000):
    import pandas as pd
    import datetime, time
    from dataLoader import dataLoaderConfig
    
    print("Start: ", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    start = time.time()

    fileEncoding = dataLoaderConfig.getEncoding()
    print(f"Reading the CSV file with '{fileEncoding}' encoding.")

    chunkIter = pd.read_csv(csvFile, chunksize=chunkSize, low_memory=False, encoding=fileEncoding)
    
    convDict = {}
    for chunk in chunkIter:
        for col in chunk.columns:
            if col in convDict:
                continue
            if chunk[col].dtype == 'object':
                try:
                    chunk[col].astype(float)
                except ValueError:
                    convDict[col] = str

    print("Converters=convDict:", {k: v.__name__ for k, v in convDict.items()})
    
    print("\nEnd: ", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print("Running: ", str(datetime.timedelta(seconds=(time.time() - start))).split(".")[0])
    print("-")
    
    return convDict

def sasWithChunks(sasFile, chunkSize=100000):
    import pyreadstat, datetime, time
    from dataLoader import dataLoaderConfig

    print("Start: ", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    start = time.time()

    fileEncoding = dataLoaderConfig.getEncoding()
    print(f"Processing the SAS file with '{fileEncoding}' encoding.")

    convDict = {}
    
    for df, meta in pyreadstat.read_file_in_chunks(pyreadstat.read_sas7bdat, sasFile, chunksize=chunkSize):
        for col in df.columns:
            if col in convDict:
                continue
            if df[col].dtype == 'object':
                try:
                    df[col].astype(float)
                except ValueError:
                    convDict[col] = str

    print("Converters=convDict:", {k: v.__name__ for k, v in convDict.items()})

    print("\nEnd: ", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print("Running: ", str(datetime.timedelta(seconds=(time.time() - start))).split(".")[0])
    print("-")
    
    return convDict