class Tee:
    def __init__(self, *streams):
        self.streams = streams

    def write(self, message):
        for stream in self.streams:
            stream.write(message)
            stream.flush()

    def flush(self):
        for stream in self.streams:
            stream.flush()

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

    with open(filePath, mode, encoding=encoding) as file:
        file.write(f"\nOutput has been redirected to {filePath}\n")

    return result, filePath
