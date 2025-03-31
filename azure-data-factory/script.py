import sys, json, os
sys.path.append("../")
from supabase_client import Data
from itertools import combinations
from dotenv import load_dotenv
load_dotenv()

from azure.storage.blob import BlobServiceClient

# Well, this function uploads files on azure:)
def upload_file_to_azure(LOCAL_FILE_PATH, BLOB_NAME):

    CONNECTION_STRING = os.getenv("AZURE_CONNECTION_STRING")
    CONTAINER_NAME = os.getenv("AZURE_CONTAINER_NAME")

    blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
    container_client = blob_service_client.get_container_client(CONTAINER_NAME)

    with open(LOCAL_FILE_PATH, "rb") as file:
        blob_client = container_client.get_blob_client(BLOB_NAME)
        blob_client.upload_blob(file, overwrite=True)
    print("File successfully uploaded!!")

# This function get all combinations for the given values:)
def helper(values):
    return [{"value1": v1, "value2": v2} for v1, v2 in combinations(values, 2)]


# Instance to get the data
data = Data()

# Method which returns all the teams that have played so far
values = data.get_teams()
res = helper(values.get("teams"))

# Writing the output in a json file
with open("input_file.json", "w") as f:
    json.dump(res, f, indent=4)

LOCAL_FILE_PATH = "input_file.json"
BLOB_NAME = "teams_combinations.json"
upload_file_to_azure(LOCAL_FILE_PATH, BLOB_NAME)
# FIle uploaded successfully(hopefully)!!