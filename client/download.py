import argparse
import os
from datetime import datetime

from google.cloud import storage

def parse_arguments():
    parser = argparse.ArgumentParser()

    # Video Args
    parser.add_argument('--download_obj',
                        action='store',
                        dest='DOWNLOAD_OBJ',
                        default='is_good_posture.xlsx')
    parser.add_argument('--destination', '--destination_path', '-d',
                        action='store',
                        dest='DESTINATION_PATH',
                        default=f'{datetime.now().strftime("%m_%d_%Y-%H_%M_%S")}.avi')
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


def download_blob(bucket_name, source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""
    # bucket_name = "your-bucket-name"
    # source_blob_name = "storage-object-name"
    # destination_file_name = "local/path/to/file"

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)

    print(
        "Blob {} downloaded to {}.".format(
            source_blob_name, destination_file_name
        )
    )

if __name__ == "__main__":
    # Set credentials https://stackoverflow.com/questions/45501082/set-google-application-credentials-in-python-project-to-use-google-api
    # JSON downloaded after clicking project here https://console.cloud.google.com/iam-admin/serviceaccounts
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "w-251-final-project.json"
    print("Download credentials set")

    args = parse_arguments()
    print("Download started")
    download_blob(args.BUCKET_NAME, args.DOWNLOAD_OBJ, args.DESTINATION_PATH)
    print("Download finished")

