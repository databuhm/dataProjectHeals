class Tee:
    
    """
    A class to duplicate the output to multiple streams.

    Args:
        *streams: Multiple stream objects (e.g., sys.stdout, file objects) where output will be written.

    Methods:
        write(message):
            Writes the given message to all streams.
        
        flush():
            Flushes all streams to ensure that all data is written.
    """
    
    def __init__(self, *streams):
        self.streams = streams

    def write(self, message):
        
        """
        Writes the message to all streams.

        Args:
            message (str): The message to be written to the streams.
        """
        
        for stream in self.streams:
            try:
                stream.write(message)
                stream.flush()
            except Exception as e:
                print(f"Error writing message to stream: {e}")

    def flush(self):
        
        """
        Flushes all streams to ensure that all buffered data is written.
        """
        
        for stream in self.streams:
            try:
                stream.flush()
            except Exception as e:
                print(f"Error flushing stream: {e}")

def redirectOutputToFile(func, outputFile:str='output.txt', mode='w', encoding='utf-8'):
    
    """
    Redirects the output of a function to a file and prints the output to the console as well.

    Args:
        func (function): The function whose output needs to be redirected.
        outputFile (str): The path of the output file where the redirected output will be saved. Default is 'output.txt'.
        mode (str): The file mode, e.g., 'w' for writing or 'a' for appending. Default is 'w'.
        encoding (str): The encoding of the output file. Default is 'utf-8'.

    Returns:
        The result of the function execution and the path of the output file.

    Raises:
        FileNotFoundError: If the output file path does not exist.
        PermissionError: If there is a permission issue while writing to the file.
        Exception: For any other unexpected errors during function execution.
    """
    
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
