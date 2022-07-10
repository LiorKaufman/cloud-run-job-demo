import requests
import pandas as pd
from os import environ
from google.cloud import storage

TASK_INDEX = environ.get("CLOUD_RUN_TASK_INDEX", 0)

def call_api(): 
    url = "https://api.publicapis.org/random"        
    resp = requests.get(url)
    return resp.json()

def upload_dataframe_as_csv(df,bucket_name, destination_blob_name):
    """Uploads a dataframe as csv file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(df.to_csv(index=False,header=True),"text/csv")

    print(
        f"{destination_blob_name} with {df.shape[0]} rows got uploaded to bucket{bucket_name}."
    )  

def main():
    print("*** Starting extraction ***") 
    data = []
    # Each call will give us a random entry from the api 
    for i in range(0,9):
        entry = call_api()
        data.append(entry["entries"][0])
    df = pd.DataFrame(data)
    upload_dataframe_as_csv(df,"my_demo_bucket_cloud_run",f"random_entries_{TASK_INDEX}.csv")

if __name__ == '__main__':
    main()
    