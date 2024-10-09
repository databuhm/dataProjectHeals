client = None

def setGbqClient(json_path=None):
    import glob, os
    from google.oauth2 import service_account
    from google.cloud import bigquery
    
    global client
    
    if client is not None:
        print("BigQuery Client is already set up.")
        return True

    try:
        if json_path is None:
            json_path = glob.glob("./*.json")[0]
        print(f"Using service account file: {json_path}")

        if not os.path.exists(json_path):
            raise FileNotFoundError(f"Service account JSON file not found at: {json_path}")
        
        credentials = service_account.Credentials.from_service_account_file(json_path)
        
        client = bigquery.Client(credentials=credentials, project=credentials.project_id)
        print(f"BigQuery Client created with project ID: {credentials.project_id}")
        return True
    
    except IndexError:
        print("Error: No service account JSON file found in the current directory or the specified path.")
        return False

    except FileNotFoundError as fnf_error:
        print(f"FileNotFoundError: {fnf_error}")
        return False

    except PermissionError:
        print("PermissionError: Permission denied to access the service account JSON file.")
        return False

    except ValueError as value_error:
        print(f"ValueError: Invalid value encountered during setup - {value_error}")
        return False

    except Exception as e:
        print(f"An unexpected error occurred during BigQuery client setup: {e}")
        return False

def getGbqClient():
    global client
    
    if client is None:
        print("BigQuery Client is not set up. Please run `setGbqClient()` first.")
    return client

def isClientInit():
    return client is not None

def resetGbqClient():
    global client
    
    client = None
    print("BigQuery Client has been reset.")
