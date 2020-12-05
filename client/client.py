import cv2
import argparse
import numpy as np
import paho.mqtt.publish as publish
import sys

from datetime import datetime
from time import sleep

def parse_arguments():
    parser = argparse.ArgumentParser()
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

    arguments = parser.parse_args()
    arguments.MQTT_PORT = int(arguments.MQTT_PORT)
    arguments.MQTT_QOS = int(arguments.MQTT_QOS)
    
    print("Supplied args:")
    [print(k,v) for k,v in arguments.__dict__.items()]

    return arguments


if __name__ == "__main__":
    args = parse_arguments()
    print("Starting video stream...")
    video_capture = cv2.VideoCapture(0)

    print(args)

    #TODO: Add video capture and publishing here

    # Default resolutions of the frame are obtained.The default resolutions are system dependent.
    # We convert the resolutions from float to integer.
    frame_width = int(video_capture.get(3))
    frame_height = int(video_capture.get(4))


    # Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
    # TODO change filename, probably change format to mp4 too
    out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))

    while(True):
        # Capture frame-by-frame.
        ret, frame = video_capture.read()

        # Throw out the color information and get the gray frame.
        # TODO maybe have in color?
        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        print("here1: " + str(ret))
        if ret == True:
            # Write the frame into the output file
            out.write(frame)

            # Display the resulting frame
            cv2.imshow('Frame', frame)
            print("here2")

            # Press Q on keyboard to stop recording
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


        # Break the loop
        else:
            break


    video_capture.release()
    out.release()
    cv2.destroyAllWindows()
