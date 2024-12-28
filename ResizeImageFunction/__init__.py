import logging
import os
from PIL import Image
import azure.functions as func
from azure.storage.blob import BlobServiceClient

def main(myblob: func.InputStream):
    logging.info(f"Python blob trigger function processed blob \n"
                 f"Name: {myblob.name}\n"
                 f"Blob Size: {myblob.length} bytes")

    # Resize image
    image = Image.open(myblob)
    image = image.resize((100, 100))  # Resize to 100x100 pixels

    # Save resized image to a temporary file
    temp_file = "/tmp/resized_image.jpg"
    image.save(temp_file)

    # Upload the resized image back to Blob Storage
    connect_str = os.getenv('AzureWebJobsStorage')
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    container_name = "mycontainer"  # Your container name
    blob_name = f"resized-{os.path.basename(myblob.name)}"
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

    with open(temp_file, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)