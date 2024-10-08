def csvWithChunks(csvFile, chunkSize=100000):
    import pandas as pd
    import datetime, time
    
    print("Start: ", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    start = time.time()

    convDict = {}
    chunkIter = pd.read_csv(csvFile, chunksize=chunkSize, low_memory=False)

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

    print("Start: ", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    start = time.time()

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