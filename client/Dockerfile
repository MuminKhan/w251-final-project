FROM nvcr.io/nvidia/l4t-ml:r32.4.3-py3

RUN apt update && \
    apt install -y \
            libffi-dev \
            python3-pip \
            python3-tk \ 
            libopencv-dev \
            python3-opencv \
            python3-numpy 
RUN pip3 install --no-cache-dir paho-mqtt
RUN pip3 install --upgrade google-cloud-storage

WORKDIR /client
COPY client.py client.py
COPY upload_to_gcp.py upload_to_gcp.py
COPY w-251-final-project.json w-251-final-project.json
COPY download.py download.py

ENV MQTT_SERVER="mqtt"
ENV MQTT_PORT=1883
ENV MQTT_TOPIC="runmo"
ENV MQTT_QOS=0

CMD ["sh", "-c", \
    "python3 -u client.py -s $MQTT_SERVER -p $MQTT_PORT -t $MQTT_TOPIC -q $MQTT_QOS && python3 -u upload_to_gcp.py && python3 -u download.py"]
