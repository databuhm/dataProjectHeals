import glob
from google.oauth2 import service_account
from google.cloud import bigquery

client = None

def SetGbqClient(json_path=None):
    global client
    
    if client is not None:
        print("BigQuery Client is already set up.")
        return True

    try:
        if json_path is None:
            json_path = glob.glob("./*.json")[0]        
        print(f"Using service account file: {json_path}")

        credentials = service_account.Credentials.from_service_account_file(json_path)
        
        client = bigquery.Client(credentials=credentials, project=credentials.project_id)
        print(f"BigQuery Client created with project ID: {credentials.project_id}")
        return True
    
    except IndexError:
        print("Error: No service account JSON file found in the specified path.")
        return False
    except Exception as e:
        print(f"An error occurred during BigQuery client setup: {e}")
        return False

def getGbqClient():
    global client
    
    if client is None:
        print("BigQuery Client is not set up. Please run `SetUpGbqClinet()` first.")
    return client

def isClientInit():
    return client is not None
