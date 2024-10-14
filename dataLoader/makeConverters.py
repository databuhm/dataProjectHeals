def getFileEncoding(filePath:str, sampleSize=100000000):
    
    """
    Detects the encoding of a file using the chardet library.
    
    Args:
        filePath (str): Path to the file for which encoding needs to be detected.
        sampleSize (int): The number of bytes to read from the file for encoding detection. Default is 100MB.
        
    Returns:
        dict: A dictionary with the file name as the key and the detected encoding as the value.
    """
    
    import chardet, os
    
    _, fileExtension = os.path.splitext(filePath)
    if fileExtension.lower() == '.sas7bdat':
        print(f"Encoding detection for '{fileExtension}' files is not supported. Returning None.")
        return None
    
    fileName = os.path.basename(filePath)
    encodingDict = {}
    
    try:
        with open(filePath, 'rb') as file:
            raw_data = file.read(sampleSize)
        
        result = chardet.detect(raw_data)
        detectedEncoding = result['encoding']
        
        if detectedEncoding is None or detectedEncoding.lower() == 'ascii':
            print(f"Detected Encoding: {detectedEncoding}. Changing to 'ISO-8859-1' for use.")
            detectedEncoding = 'ISO-8859-1'
        
        encodingDict[fileName] = detectedEncoding
        print(f"Final encoding to be used for '{fileName}': {detectedEncoding}")
    
    except Exception as e:
        print(f"Error occurred while detecting encoding for '{fileName}': {e}. Using default 'ISO-8859-1'.")
        detectedEncoding = 'ISO-8859-1'
        encodingDict[fileName] = detectedEncoding
    
    return encodingDict

def getMultiFileEncodings(csvDirPath:str, defaultEncoding:str='iso-8859-1'):
    
    """
    Detects the encoding of multiple CSV files in a directory.
    
    Args:
        csvDirPath (str): The directory containing CSV files.
        defaultEncoding (str): Default encoding to use if detection fails or if 'ascii' is detected. Default is 'iso-8859-1'.
        
    Returns:
        dict: A dictionary with file names as keys and detected encodings as values.
    """
    
    import os
    import chardet
    
    encodings = {}
    csvList = sorted([file for file in os.listdir(csvDirPath) if file.endswith('.csv')])
    
    for csvFile in csvList:
        filePath = os.path.join(csvDirPath, csvFile)
        fileExtension = os.path.splitext(csvFile)[1].lower()
        
        if fileExtension == '.sas7bdat':
            encodings[csvFile] = 'File type not applicable for encoding detection'
            print(f"Skipping encoding detection for '{csvFile}' as it is a '.sas7bdat' file.")
            continue
        
        try:
            with open(filePath, 'rb') as file:
                raw_data = file.read(100000000)
                result = chardet.detect(raw_data)
                encoding = result['encoding']
                
                if encoding is None or encoding.lower() == 'ascii':
                    print(f"File '{csvFile}' detected as 'ascii'. Using default encoding '{defaultEncoding}'.")
                    encoding = defaultEncoding
                
                encodings[csvFile] = encoding
                print(f"File '{csvFile}' encoding detected: {encoding}")
        
        except Exception as e:
            print(f"Error detecting encoding for file '{csvFile}': {e}")
            encodings[csvFile] = 'Unknown'
    
    return encodings

def csvWithChunks(csvFile:str, chunkSize:int=100000, encodingDict:dict=None):
    
    """
    Reads a CSV file in chunks and detects column data types, converting object columns to strings.
    
    Args:
        csvFile (str): The path to the CSV file.
        chunkSize (int): The number of rows per chunk. Default is 100,000 rows.
        encodingDict (dict): A dictionary of file names and their corresponding encodings.
        
    Returns:
        dict: A dictionary with column names as keys and data types (str or float) as values.
    """
    
    import pandas as pd
    import datetime, time, os

    print("Start:", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    start = time.time()
    
    fileName = os.path.basename(csvFile)

    if encodingDict and fileName in encodingDict:
        fileEncoding = encodingDict[fileName]
    else:
        print(f"Warning: Encoding for '{fileName}' not provided. Using default 'ISO-8859-1'.")
        fileEncoding = 'ISO-8859-1'

    print(f"Reading the CSV file '{fileName}' with '{fileEncoding}' encoding.")
    
    try:
        chunkIter = pd.read_csv(csvFile, chunksize=chunkSize, low_memory=False, encoding=fileEncoding)
    except UnicodeDecodeError as e:
        print(f"UnicodeDecodeError: {e}. Retrying with 'ISO-8859-1' encoding.")
        chunkIter = pd.read_csv(csvFile, chunksize=chunkSize, low_memory=False, encoding='ISO-8859-1')

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

    print("End:", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print("Running:", str(datetime.timedelta(seconds=(time.time() - start))).split(".")[0])
    
    return convDict

def sasWithChunks(sasFile:str, chunkSize:int=100000):
    
    """
    Reads a SAS file in chunks and detects column data types.
    
    Args:
        sasFile (str): The path to the SAS file.
        chunkSize (int): The number of rows per chunk. Default is 100,000 rows.
        
    Returns:
        dict: A dictionary with column names as keys and their corresponding data types (str or float).
    """
    
    import pyreadstat, datetime, time, os

    print("Start:", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    start = time.time()

    fileName = os.path.basename(sasFile)
    print(f"Processing the SAS file '{fileName}' with default encoding (encoding is handled by pyreadstat based on file metadata).")

    convDict = {}
    
    try:
        for i, (df, meta) in enumerate(pyreadstat.read_file_in_chunks(pyreadstat.read_sas7bdat, sasFile, chunksize=chunkSize)):
            print(f"Processing chunk {i+1} with shape: {df.shape}")

            for col in df.columns:
                if col in convDict:
                    continue
                if df[col].dtype == 'object':
                    try:
                        df[col].astype(float)
                    except ValueError:
                        convDict[col] = str

    except FileNotFoundError:
        print(f"Error: The SAS file '{sasFile}' was not found.")
        return {}
    except UnicodeDecodeError as e:
        print(f"UnicodeDecodeError occurred: {e}.")
        return {}
    except Exception as e:
        print(f"An unexpected error occurred: {e}.")
        return {}

    print("End:", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print("Running:", str(datetime.timedelta(seconds=(time.time() - start))).split(".")[0])
    print()

    return convDict