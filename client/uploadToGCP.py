# https://cloud.google.com/storage/docs/reference/libraries
from google.cloud import storage

print("test output for GCP py file")

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
create_bucket("test_bucket")
upload_blob("test_bucket", "outpy.avi", "nx_output.avi")
