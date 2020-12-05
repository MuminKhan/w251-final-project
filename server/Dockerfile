FROM google/cloud-sdk:alpine


RUN pip3 install --no-cache-dir \
        paho-mqtt

WORKDIR /subscribe
COPY subscription.py subscription.py

CMD ["python3", "-u", "subscription.py"]
