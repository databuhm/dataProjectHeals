class Tee:
    def __init__(self, *streams):
        self.streams = streams

    def write(self, message):
        for stream in self.streams:
            try:
                stream.write(message)
                stream.flush()  # 실시간 기록 보장
            except Exception as e:
                print(f"Error writing message to stream: {e}")

    def flush(self):
        for stream in self.streams:
            try:
                stream.flush()
            except Exception as e:
                print(f"Error flushing stream: {e}")

def redirectOutputToFile(func, filePath='output.txt', mode='w', encoding='utf-8'):
    import sys
    import os
    
    dirName = os.path.dirname(filePath)
    
    if dirName and not os.path.exists(dirName):
        try:
            os.makedirs(dirName)
            print(f"Directory '{dirName}' created for output file.")
        except OSError as e:
            print(f"Error: Could not create directory '{dirName}': {e}")
            return None, filePath

    originStdOut = sys.stdout
    
    try:
        with open(filePath, mode, encoding=encoding) as file:
            sys.stdout = Tee(file, originStdOut)
            result = func()
    except FileNotFoundError as e:
        print(f"Error: File '{filePath}' not found. Exception: {e}")
        result = None
    except PermissionError as e:
        print(f"Error: Permission denied when accessing '{filePath}'. This might be caused by the file being open in another program. Exception: {e}")
        result = None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        result = None
    finally:
        sys.stdout = originStdOut
        print(f"Output redirection completed. Original stdout restored.")
        
        try:
            with open(filePath, 'a', encoding=encoding) as file:  # 'a' 모드로 파일 접근
                file.write(f"\nOutput has been redirected to {filePath}\n")
        except Exception as e:
            print(f"Error writing final log to file '{filePath}': {e}")

    return result, filePath
