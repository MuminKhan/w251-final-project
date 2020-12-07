import datetime
import math
from time import sleep

import pandas as pd
from google.cloud import videointelligence_v1p3beta1 as videointelligence
from google.cloud import storage

from trig import *


def detect_person(gcs_uri):
    """
    Detects people in a video with Google Video Intelligence
    """

    client = videointelligence.VideoIntelligenceServiceClient()

    # Configure the request
    config = videointelligence.types.PersonDetectionConfig(
        include_bounding_boxes=True,
        include_attributes=True,
        include_pose_landmarks=True,
    )
    context = videointelligence.types.VideoContext(
        person_detection_config=config)

    # Start the asynchronous request
    operation = client.annotate_video(
        request={
            "features": [videointelligence.Feature.PERSON_DETECTION],
            "input_uri": gcs_uri,
            "video_context": context,
        }
    )

    print("\nProcessing video for person detection annotations.")
    result = operation.result(timeout=300)

    print("\nFinished processing.\n")
    return result


def analyze_person(person):
    """
    Converts Google VideoIntellegence object to timesteamp-keyed dict
    """
    frames = []
    for track in person.tracks:
        # Convert timestamps to seconds
        for timestamped_object in track.timestamped_objects:
            timestamp = timestamped_object.time_offset.total_seconds()
            frame = {'timestamp': timestamp}

            timestamped_object = track.timestamped_objects[0]

            for landmark in timestamped_object.landmarks:
                frame[landmark.name + '_x'] = landmark.point.x
                frame[landmark.name + '_y'] = 1 - landmark.point.y

            frames.append(frame)
            
    sorted(frames, key=lambda x: x['timestamp'])
    return frames


def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # bucket_name = "your-bucket-name"
    # source_file_name = "local/path/to/file"
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print("File {} uploaded to {}.".format(
        source_file_name, destination_blob_name))


def main(event, context):
    """
    Google Cloud Function entrypoint
    """
    print('Event ID: {}'.format(context.event_id))
    print('Event type: {}'.format(context.event_type))

    input_uri = f'gs://{event["bucket"]}/{event["name"]}'

    result = detect_person(input_uri)
    people_annotations = result.annotation_results[0].person_detection_annotations

    annotationsPd = pd.DataFrame(analyze_person(people_annotations[0]))
    for annotation in people_annotations[1:]:
        annotationsPd = annotationsPd.append(pd.DataFrame(analyze_person(annotation)))

    annotationsPd = annotationsPd.sort_values('timestamp', ascending=True)

    annotationsPd['right_elbow_angle'] = annotationsPd.apply(computeRightElbowAngle, axis=1)
    annotationsPd['right_shoulder_angle'] = annotationsPd.apply(computeRightShoulderAngle, axis=1)
    annotationsPd['right_knee_angle'] = annotationsPd.apply(computeRightKneeAngle, axis=1)

    annotationsPd['left_elbow_angle'] = annotationsPd.apply(computeLeftElbowAngle, axis=1)
    annotationsPd['left_shoulder_angle'] = annotationsPd.apply(computeLeftShoulderAngle, axis=1)
    annotationsPd['left_knee_angle'] = annotationsPd.apply(computeLeftKneeAngle, axis=1)

    annotationsPd['back_angle'] = annotationsPd.apply(computeBackAngle, axis=1)
    annotationsPd['stride_length'] = annotationsPd.apply(computeStrideLength, axis=1)
    annotationsPd['ideal_stride'] = annotationsPd.apply(computeIdealStrideLength, axis=1)
    annotationsPd['is_good_posture'] = annotationsPd.apply(isGoodPosture, axis=1)

    file_to_write = 'is_good_posture.xlsx'
    excel_to_write = annotationsPd.to_excel(file_to_write)
    upload_blob("w251_test", excel_to_write, file_to_write)
