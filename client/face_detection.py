import numpy as np
import cv2
import paho.mqtt.client as mqtt
import time

# Create a new client instance and connect to the local broker.
#client = mqtt.Client()
LOCAL_MQTT_BROKER = "jetson_mqtt_broker"
LOCAL_MQTT_PORT = 1883
LOCAL_MQTT_TOPIC = "faces"
#LOCAL_MQTT_TOPIC = "hw3_topic/local"
client = mqtt.Client()
#client.connect("172.18.0.2")

# Default flag
flag_connected = 0

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("connected to broker")
    else:
        print("BAD CONNECTION RETURNED CODE =",rc)


print('----------- Checkpoint 1 -----------')
#client.connect("172.18.0.2")
client.connect(LOCAL_MQTT_BROKER, LOCAL_MQTT_PORT, 60)
print('----------- Checkpoint 2 -----------')
client.on_connect = on_connect
#client.on_disconnect = on_disconnect

# Use the web camera to capture frame.
cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame.
    ret, frame = cap.read()
    # Throw out the color information and get the gray frame.
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Face detection.
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    #faces = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    if len(faces) > 0:
        print('---------------- Face(s) detected')
    else:
        print('No face detected')

    for (x,y,w,h) in faces:

        face = frame[y:y+h, x:x+w]

        rc, jpg=cv2.imencode('.png', face)
        if rc:
            print('face encoded successfully')
	
        msg = jpg.tobytes()

        # Publish a message
        if flag_connected == 1:
            print('Publishing messages')
            client.publish(LOCAL_MQTT_TOPIC, msg)
            #client.publish("faces_detected", payload=msg)
        else:
            print('MESSAGE NOT PUBLISHED TO MQTT BROKER')

        #client.publish("faces_detected", payload=msg)

        # display the frame with detected faces
        #cv2.imshow('frame', frame)

        cv2.waitKey(1)
        break
        
cap.release()
cv2.destroyAllWindows()
