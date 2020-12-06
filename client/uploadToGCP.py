# https://cloud.google.com/storage/docs/reference/libraries
import os
from google.cloud import storage

print("test output for GCP py file")

# Set credentials https://stackoverflow.com/questions/45501082/set-google-application-credentials-in-python-project-to-use-google-api
# JSON downloaded after clicking project here https://console.cloud.google.com/iam-admin/serviceaccounts
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="w-251-final-project.json"
print("set Google credentials")

def create_bucket(bucket_name):
    # Instantiates a client
    storage_client = storage.Client()

    # Creates the new bucket
    bucket = storage_client.create_bucket(bucket_name)

    print("Bucket {} created.".format(bucket.name))

# https://cloud.google.com/storage/docs/uploading-objects#storage-upload-object-python
def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # bucket_name = "your-bucket-name"
    # source_file_name = "local/path/to/file"
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )


# TODO make this not hard-coded?
upload_blob("w251_test", "outpy.avi", "nx_output.avi")
