import argparse
from datetime import datetime

import paho.mqtt.client as mqtt
from google.cloud import storage


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--server', '--mqtt_server', '-s',
                        action='store',
                        dest='MQTT_SERVER',
                        default='mqtt')
    parser.add_argument('--port', '--mqtt_port', '-p',
                        action='store',
                        dest='MQTT_PORT',
                        default=1883)
    parser.add_argument('--topic', '--mqtt_topic', '-t',
                        action='store',
                        dest='MQTT_TOPIC',
                        default='runmo')
    parser.add_argument('--bucket',
                        action='store',
                        dest='BUCKET',
                        default='w251-hw3')
    parser.add_argument('--key',
                        action='store',
                        dest='KEY',
                        default='runmo')

    arguments = parser.parse_args()
    arguments.MQTT_PORT = int(arguments.MQTT_PORT)

    print("Supplied args:")
    [print(k, v) for k, v in arguments.__dict__.items()]

    return arguments


def upload_blob(file_obj, bucket_name, destination_blob_name):
    """This is just an example. Fix this method to work with the MQTT message.
    Uploads a file to the bucket."""
    # bucket_name = "your-bucket-name"
    # destination_blob_name = "storage-object-name"
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # https://googleapis.dev/python/storage/latest/blobs.html#google.cloud.storage.blob.Blob.upload_from_file
    blob.upload_from_file(file_obj)


def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {str(rc)}")
    client.subscribe(args.MQTT_TOPIC)


def on_message(client, userdata, msg):
    cur_time = datetime.now().strftime("%m_%d_%Y-%H_%M_%S")
    out_file = f'{cur_time}.mp4'
    msg = bytes(msg.payload)
    upload_blob(msg, args.BUCKET, f'{args.KEY}\{out_file}')


if __name__ == "__main__":
    args = parse_arguments()
    storage_client = storage.Client()

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(args.MQTT_SERVER, args.MQTT_PORT, 60)
    client.loop_forever()
