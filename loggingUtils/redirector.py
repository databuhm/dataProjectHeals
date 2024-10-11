class Tee:
    def __init__(self, *streams):
        self.streams = streams

    def write(self, message):
        for stream in self.streams:
            try:
                stream.write(message)
                stream.flush()
            except Exception as e:
                print(f"Error writing message to stream: {e}")

    def flush(self):
        for stream in self.streams:
            try:
                stream.flush()
            except Exception as e:
                print(f"Error flushing stream: {e}")

def redirectOutputToFile(func, outputFile:str='output.txt', mode='w', encoding='utf-8'):
    '''
    usage: redirectOutPutToFile(lambda FUNC(params), outputFile))
    '''
    import sys
    import os
    
    dirName = os.path.dirname(outputFile)
    
    if dirName and not os.path.exists(dirName):
        try:
            os.makedirs(dirName)
            print(f"Directory '{dirName}' created for output file.")
        except OSError as e:
            print(f"Error: Could not create directory '{dirName}': {e}")
            return None, outputFile

    originStdOut = sys.stdout
    
    try:
        with open(outputFile, mode, encoding=encoding) as file:
            sys.stdout = Tee(file, originStdOut)
            result = func()
    except FileNotFoundError as e:
        print(f"Error: File '{outputFile}' not found. Exception: {e}")
        result = None
    except PermissionError as e:
        print(f"Error: Permission denied when accessing '{outputFile}'. This might be caused by the file being open in another program. Exception: {e}")
        result = None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        result = None
    finally:
        sys.stdout = originStdOut
        print(f"Output redirection completed. Original stdout restored.")
        
        try:
            with open(outputFile, 'a', encoding=encoding) as file:
                file.write(f"\nOutput has been redirected to {outputFile}\n")
        except Exception as e:
            print(f"Error writing final log to file '{outputFile}': {e}")

    return result, outputFile
