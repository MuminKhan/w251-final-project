import datetime
from time import sleep

import pandas as pd
from google.cloud import videointelligence_v1p3beta1 as videointelligence


def detect_person(gcs_uri):
    """Detects people in a video."""

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


def main(event, context):
    """Google Function entrypoint
    """
    print('Event ID: {}'.format(context.event_id))
    print('Event type: {}'.format(context.event_type))

    input_uri = f'gs://{event["bucket"]}/{event["name"]}'

    result = detect_person(input_uri)
    people_annotations = result.annotation_results[0].person_detection_annotations

    annotationsPd = pd.DataFrame(analyzePerson(people_annotations[0]))
    for annotation in people_annotations[1:]:
        annotationsPd = annotationsPd.append(pd.DataFrame(analyzePerson(annotation)))

    annotationsPd = annotationsPd.sort_values('timestamp', ascending=True)

    return annotationsPd
