def makeBigQueryDataset(datasetName:str='dataBigQuery'):
    from google.cloud import bigquery
    from gbqLoader.gbqConfig import getGbqClient
    """
    Create a BigQuery dataset with the specified name.
    Args:
        datasetName (str): The name of the dataset to create.
    Returns:
        bool: True if the dataset is created successfully, False otherwise.
    """
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
    from google.cloud import bigquery
    from gbqLoader.gbqConfig import getGbqClient
    """
    Load the DataFrames in dfDict into BigQuery tables within the specified dataset.
    Args:
        datasetName (str): The name of the dataset where tables will be created.
        dfDict (dict): A dictionary where keys are table names and values are DataFrames.
    Returns:
        bool: True if all tables are created and data is loaded successfully, False otherwise.
    """
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
