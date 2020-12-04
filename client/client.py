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

    """
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    while True:
        ret, frame = video_capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor = 1.1, minNeighbors = 8)

        for (x, y, w, h) in faces:
            gray = gray[y:y+h, x:x+w]
            cv2.rectangle(gray, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cur_time = datetime.now().strftime("%m_%d_%Y-%H_%M_%S")
            out_file = f'{cur_time}.png'
            #cv2.imwrite(out_file, gray)
            #print(f'Face found! Written to {out_file}')
            
            encoded_img = cv2.imencode('.png', gray)[1].tobytes()
            publish.single(args.MQTT_TOPIC, payload=encoded_img, hostname=args.MQTT_SERVER, port=args.MQTT_PORT, qos=args.MQTT_QOS)
            print(f'Published {out_file} to {args.MQTT_SERVER}:{args.MQTT_PORT} topic: {args.MQTT_TOPIC}')
            sleep(5)

        #cv2.imshow('Video', frame)
        #if cv2.waitKey(1) & 0xFF == ord('q'):
        #    break
    """

    #TODO: Add video capture and publishing here

    video_capture.release()
    cv2.destroyAllWindows()
