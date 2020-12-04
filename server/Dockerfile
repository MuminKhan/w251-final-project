FROM alpine:latest


RUN apk add --no-cache \
        python3 \
        py3-pip && \
    pip install --no-cache-dir \
        boto3 \
        paho-mqtt

WORKDIR /subscribe
COPY subscription.py subscription.py

CMD ["python3", "-u", "subscription.py"]
