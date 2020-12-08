import argparse
import os
from datetime import datetime

from google.cloud import storage


def parse_arguments():
    parser = argparse.ArgumentParser()

    # Video Args
    parser.add_argument('--upload_obj',
                        action='store',
                        dest='UPLOAD_OBJ',
                        default='outpy.avi')
    parser.add_argument('--destination', '--destination_path', '-d',
                        action='store',
                        dest='DESTINATION_PATH',
                        default=f'{datetime.now().strftime("%m_%d_%Y-%H_%M_%S")}.xlsx')
    parser.add_argument('--bucket', '--bucket_name', '-b',
                        action='store',
                        dest='BUCKET_NAME',
                        default='w251_test')

    arguments = parser.parse_args()
    # arguments.MQTT_PORT = int(arguments.MQTT_PORT)
    # arguments.MQTT_QOS = int(arguments.MQTT_QOS)

    print("Supplied args:")
    [print(k, v) for k, v in arguments.__dict__.items()]

    return arguments


def create_bucket(bucket_name):
    # https://cloud.google.com/storage/docs/uploading-objects#storage-upload-object-python
    # Instantiates a client
    storage_client = storage.Client()

    # Creates the new bucket
    bucket = storage_client.create_bucket(bucket_name)

    print("Bucket {} created.".format(bucket.name))


def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # bucket_name = "your-bucket-name"
    # source_file_name = "local/path/to/file"
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print("File {} uploaded to {}.".format(
        source_file_name, destination_blob_name))


if __name__ == "__main__":
    # Set credentials https://stackoverflow.com/questions/45501082/set-google-application-credentials-in-python-project-to-use-google-api
    # JSON downloaded after clicking project here https://console.cloud.google.com/iam-admin/serviceaccounts
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "w-251-final-project.json"
    print("Upload credentials set")

    args = parse_arguments()
    print("Upload started")

    upload_blob(args.BUCKET_NAME, args.UPLOAD_OBJ, args.DESTINATION_PATH)

    print("Upload finished")
