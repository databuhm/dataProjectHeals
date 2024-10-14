def makeBigQueryDataset(datasetName:str='dataBigQuery'):
    
    """
    Creates BigQuery datasets with the specified name.
    
    Args:
        datasetName (str): The name of the dataset to create.
        
    Returns:
        bool: True if the dataset is successfully created, False otherwise.
    """
    
    from google.cloud import bigquery
    from gbqLoader.gbqConfig import getGbqClient

    client = getGbqClient()
    
    if client is None:
        print("Error: BigQuery client is not initialized. Please run `setGbqClient()` first.")
        return False
    
    try:
        datasetID = f"{client.project}.{datasetName}"
        dataset = bigquery.Dataset(datasetID)
        dataset.location = "US"
        dataset = client.create_dataset(dataset, exists_ok=True)

        print(f"Dataset '{datasetName}' created successfully.")
        return True

    except Exception as e:
        print(f"Failed to create dataset '{datasetName}': {e}")
        return False

def loadDataFrameToBigQuery(datasetName:str, dfDict:dict):
    
    """
    Loads DataFrames from a dictionary into BigQuery tables within the specified dataset.
    
    Args:
        datasetName (str): The name of the BigQuery dataset where the tables will be created.
        dfDict (dict): A dictionary where keys are table names and values are DataFrames.
        
    Returns:
        bool: True if all DataFrames are successfully loaded, False otherwise.
    """
    
    from google.cloud import bigquery
    from gbqLoader.gbqConfig import getGbqClient

    client = getGbqClient()
    
    if client is None:
        print("Error: BigQuery client is not initialized. Please run `setGbqClient()` first.")
        return False
    
    try:
        for tableName, df in dfDict.items():
            tableID = f"{client.project}.{datasetName}.{tableName}"
            jobConfig = bigquery.LoadJobConfig()
            
            jobConfig.schema = [bigquery.SchemaField(col, "STRING") for col in df.columns]
            jobConfig.write_disposition = bigquery.WriteDisposition.WRITE_TRUNCATE
            
            loadJob = client.load_table_from_dataframe(df.astype(str), tableID, job_config=jobConfig)
            loadJob.result()
            
            print(f"Table '{tableName}' loaded successfully into dataset '{datasetName}'.")

        return True

    except Exception as e:
        print(f"Failed to load DataFrame to BigQuery: {e}")
        return False
