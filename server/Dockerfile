FROM alpine:latest


RUN apk add --no-cache \
        python3 \
        py3-pip && \
    pip install --no-cache-dir \
        pip install google-cloud-storage \
        paho-mqtt

WORKDIR /subscribe
COPY subscription.py subscription.py

CMD ["python3", "-u", "subscription.py"]
