# 전역 변수를 선언하여 인코딩 값을 저장할 수 있도록 설정
file_encoding = None

def getFileEncoding(filePath, sampleSize=100000):
    """
    파일의 인코딩을 확인하고, 이를 올바르게 읽을 수 있는 판다스의 인코딩 옵션을 리턴하는 함수.
    인코딩 값을 전역 변수로 설정하여 이후의 함수에서 사용할 수 있도록 함.
    
    Args:
        filePath (str): 인코딩을 확인할 파일 경로
        sampleSize (int): 인코딩 감지에 사용할 바이트 크기 (기본값: 100,000)
    
    Returns:
        str: 판다스의 인코딩 옵션으로 사용할 인코딩 타입
    """
    import chardet
    global file_encoding  # 전역 변수로 선언하여 다른 함수에서도 접근 가능하도록 설정

    try:
        with open(filePath, 'rb') as file:
            raw_data = file.read(sampleSize)
        
        result = chardet.detect(raw_data)
        detectedEncoding = result['encoding']
        
        # ASCII 인코딩일 경우 ISO-8859-1로 변경
        if detectedEncoding is None or detectedEncoding.lower() == 'ascii':
            print(f"Detected Encoding: {detectedEncoding}. 'ISO-8859-1'로 변경하여 사용합니다.")
            file_encoding = 'ISO-8859-1'
        else:
            print(f"감지된 파일 인코딩: {detectedEncoding}")
            file_encoding = detectedEncoding
    
    except Exception as e:
        print(f"인코딩 감지 중 오류 발생: {e}. 기본값 'ISO-8859-1'을 사용합니다.")
        file_encoding = 'ISO-8859-1'
    
    return file_encoding


def csvWithChunks(csvFile, chunkSize=100000):
    """
    감지된 인코딩을 사용하여 CSV 파일을 청크 단위로 읽고, 변환 딕셔너리를 생성하는 함수.
    
    Args:
        csvFile (str): CSV 파일 경로
        chunkSize (int): 청크 단위로 데이터를 읽어들일 행 수 (기본값: 100,000)
    
    Returns:
        dict: 데이터 유형 변환을 위한 딕셔너리
    """
    import pandas as pd
    import datetime, time
    global file_encoding  # 전역 변수 file_encoding 사용

    print("Start: ", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    start = time.time()

    # 감지된 인코딩을 사용하여 CSV 파일을 청크 단위로 읽기
    chunkIter = pd.read_csv(csvFile, chunksize=chunkSize, low_memory=False, encoding=file_encoding)
    
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
    """
    감지된 인코딩을 사용하여 SAS 파일을 청크 단위로 읽고, 변환 딕셔너리를 생성하는 함수.
    
    Args:
        sasFile (str): SAS 파일 경로
        chunkSize (int): 청크 단위로 데이터를 읽어들일 행 수 (기본값: 100,000)
    
    Returns:
        dict: 데이터 유형 변환을 위한 딕셔너리
    """
    import pyreadstat, datetime, time
    global file_encoding  # 전역 변수 file_encoding 사용 (pyreadstat은 인코딩이 필요하지 않으므로 참조만)

    print("Start: ", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    start = time.time()

    convDict = {}
    
    # pyreadstat은 인코딩 옵션을 받지 않기 때문에, 감지된 인코딩을 참조만 합니다.
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
