def getFileEncoding(filePath, sampleSize=100000000):
    import chardet
    from dataLoader import globalConfig

    try:
        with open(filePath, 'rb') as file:
            raw_data = file.read(sampleSize)
        
        result = chardet.detect(raw_data)
        detectedEncoding = result['encoding']
        
        if detectedEncoding is None or detectedEncoding.lower() == 'ascii':
            print(f"Detected Encoding: {detectedEncoding}. 'ISO-8859-1'로 변경하여 사용합니다.")
            globalConfig.setEncoding('ISO-8859-1')
        else:
            print(f"감지된 파일 인코딩: {detectedEncoding}")
            globalConfig.setEncoding(detectedEncoding)
    
    except Exception as e:
        print(f"인코딩 감지 중 오류 발생: {e}. 기본값 'ISO-8859-1'을 사용합니다.")
        globalConfig.setEncoding('ISO-8859-1')
    
    return globalConfig.getEncoding()

def csvWithChunks(csvFile, chunkSize=100000):
    import pandas as pd
    import datetime, time
    from dataLoader import globalConfig
    
    print("Start: ", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    start = time.time()

    fileEncoding = globalConfig.getEncoding()
    print(f"CSV 파일을 '{fileEncoding}' 인코딩으로 읽습니다.")

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
    from dataLoader import globalConfig

    print("Start: ", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    start = time.time()

    fileEncoding = globalConfig.getEncoding()
    print(f"SAS 파일을 '{fileEncoding}' 인코딩으로 처리합니다.")

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
