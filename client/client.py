import argparse
import sys
import time
from datetime import datetime

import cv2
import paho.mqtt.publish as publish


def parse_arguments():
    parser = argparse.ArgumentParser()

    # MQTT Args
    parser.add_argument('--server', '--mqtt_server', '-s',
                        action='store',
                        dest='MQTT_SERVER',
                        required=True)
    parser.add_argument('--port', '--mqtt_port', '-p',
                        action='store',
                        dest='MQTT_PORT',
                        default=1883)
    parser.add_argument('--qos', '--mqtt_qos', '-q',
                        action='store',
                        dest='MQTT_QOS',
                        default=0)
    parser.add_argument('--topic', '--mqtt_topic', '-t',
                        action='store',
                        dest='MQTT_TOPIC',
                        default='runmo')

    # Video Args
    parser.add_argument('--length', '--video_length', '-l',
                        action='store',
                        dest='VIDEO_LENGTH',
                        default=10)
    parser.add_argument('--output', '--output_name', '-o',
                        action='store',
                        dest='VIDEO_OUTPUT',
                        default='outpy.avi')

    arguments = parser.parse_args()
    arguments.MQTT_PORT = int(arguments.MQTT_PORT)
    arguments.MQTT_QOS = int(arguments.MQTT_QOS)

    print("Supplied args:")
    [print(k, v) for k, v in arguments.__dict__.items()]

    return arguments


if __name__ == "__main__":
    args = parse_arguments()
    print("Starting video stream...")
    video_capture = cv2.VideoCapture(0)

    print(args)

    # Default resolutions of the frame are obtained.The default resolutions are system dependent.
    frame_width = int(video_capture.get(3))
    frame_height = int(video_capture.get(4))

    # Define the codec and create VideoWriter object. The output is stored in args.VIDEO_OUTPUT.
    out = cv2.VideoWriter(
        args.VIDEO_OUTPUT,
        cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'),
        10,
        (frame_width, frame_height)
    )

    start_time = time.time()

    video_length = args.VIDEO_LENGTH
    last_time_left = -1
    while(time.time() - start_time < video_length):
        time_left = video_length - int(time.time() - start_time)

        if time_left != last_time_left:
            print("Approximate time left: " + str(time_left))
            last_time_left = time_left

        # Capture frame-by-frame.
        return_val, frame = video_capture.read()
        if return_val is None or not return_val:
            break
        out.write(frame)
        cv2.imshow('Frame', frame)

        # stops when you press the 'Q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    out.release()
    cv2.destroyAllWindows()
