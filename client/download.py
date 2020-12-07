from google.cloud import storage

# Initialise a client
storage_client = storage.Client("[project name]")

# Create a bucket object for our bucket
bucket = storage_client.get_bucket(bucket_name)

# Create a blob object from the filepath
blob = bucket.blob("folder/filename.extension")

# Download the file to a destination
blob.download_to_filename(destination_file_name)