#import json
#import math
#import os
#import sys
from time import sleep

#import numpy as np
#import pandas as pd
#from google.cloud import automl
from google.cloud import videointelligence_v1p3beta1 as videointelligence
#from google.colab import auth, files
#from google.oauth2 import service_account
##from matplotlib import pyplot as plt
#from PIL import Image, ImageDraw

#from trig import *


def detect_person(input_uri):
    """Detects people in a video."""

    # client = videointelligence.VideoIntelligenceServiceClient(
    #    credentials=service_account.Credentials.from_service_account_file('./key.json'))
    client = videointelligence.VideoIntelligenceServiceClient()

    # Configure the request
    config = videointelligence.types.PersonDetectionConfig(
        include_bounding_boxes=True,
        include_attributes=True,
        include_pose_landmarks=True,
    )
    context = videointelligence.types.VideoContext(
        person_detection_config=config)

    # Docs: https://googleapis.dev/python/videointelligence/latest/videointelligence_v1p3beta1/services.html
    # Start the asynchronous request
    operation = client.annotate_video(
        input_uri=input_uri,
        # originally was [videointelligence.enums.Feature.PERSON_DETECTION]
        features=[videointelligence.Feature.PERSON_DETECTION],
        # video_context=context
    )

    return operation


def analyzePerson(person):
    '''
    This helper function takes in a person and rearranges the data so it's in
    a timeline, which will make it easier for us to work with
    '''
    frames = []
    for track in person['tracks']:
        # Convert timestamps to seconds
        for ts_obj in track['timestamped_objects']:
            time_offset = ts_obj['time_offset']
            timestamp = 0
            if 'nanos' in time_offset:
                timestamp += time_offset['nanos'] / 10**9
            if 'seconds' in time_offset:
                timestamp += time_offset['seconds']
            if 'minutes' in time_offset:
                timestamp += time_offset['minutes'] * 60
            frame = {'timestamp': timestamp}

            # for debugging
            # print(ts_obj)

            # Added try/catch for objects without landmarks
            try:
                for landmark in ts_obj['landmarks']:
                    frame[landmark['name'] + '_x'] = landmark['point']['x']
                    # Subtract y value from 1 because positions are calculated
                    # from the top left corner
                    frame[landmark['name'] + '_y'] = 1 - \
                        landmark['point']['y']
            except KeyError:
                print("Timestamp object " +
                      str(ts_obj['time_offset']) + " does not have a landmarks object")
            frames.append(frame)
    sorted(frames, key=lambda x: x['timestamp'])
    return frames


def main(event, context):
    """Google Function entrypoint
    """
    print('Event ID: {}'.format(context.event_id))
    print('Event type: {}'.format(context.event_type))

    input_uri = f'gs://{event["bucket"]}/{event["name"]}'

    response = detect_person(input_uri)

    while not response.done():
        print(
            f"Video annotation ${response.operation.name} is still executing...")
        sleep(15)

    print(f"Video annotation ${response.operation.name} is done!")
    result = response.result()

    labels = result.annotation_results[0].person_detection_annotations
    print(labels)

    """
    annotationsPd = pd.DataFrame(analyzePerson(people_annotations[0]))
    for annotation in people_annotations[1:]:
        annotationsPd = annotationsPd.append(
            pd.DataFrame(analyzePerson(annotation)))

    annotationsPd = annotationsPd.sort_values('timestamp', ascending=True)

    annotationsPd['right_elbow_angle'] = annotationsPd.apply(computeRightElbowAngle, axis=1)
    annotationsPd['right_shoulder_angle'] = annotationsPd.apply(computeRightShoulderAngle, axis=1)
    annotationsPd['right_knee_angle'] = annotationsPd.apply(computeRightKneeAngle, axis=1)

    annotationsPd['left_elbow_angle'] = annotationsPd.apply(computeLeftElbowAngle, axis=1)
    annotationsPd['left_shoulder_angle'] = annotationsPd.apply(computeLeftShoulderAngle, axis=1)
    annotationsPd['left_knee_angle'] = annotationsPd.apply(computeLeftKneeAngle, axis=1)

    annotationsPd['back_angle'] = annotationsPd.apply(computeBackAngle, axis=1)

    #? I don't know whhhhhhhhhhhhhhat is happening
    """
