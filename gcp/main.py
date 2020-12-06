import datetime
import math
import pandas as pd
from time import sleep
from google.cloud import videointelligence_v1p3beta1 as videointelligence

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def getAngle(a, b, c):
    ang = math.degrees(math.atan2(c.y-b.y, c.x-b.x) -
                       math.atan2(a.y-b.y, a.x-b.x))
    return ang


def computeRightElbowAngle(row):
    wrist = Point(row[f'right_wrist_x'], row[f'right_wrist_y'])
    elbow = Point(row[f'right_elbow_x'], row[f'right_elbow_y'])
    shoulder = Point(row[f'right_shoulder_x'], row[f'right_shoulder_y'])
    return getAngle(wrist, elbow, shoulder)

def computeRightShoulderAngle(row):
    elbow = Point(row[f'right_elbow_x'], row[f'right_elbow_y'])
    shoulder = Point(row[f'right_shoulder_x'], row[f'right_shoulder_y'])
    hip = Point(row[f'right_hip_x'], row[f'right_hip_y'])
    return getAngle(hip, shoulder, elbow)


def computeRightKneeAngle(row):
    hip = Point(row[f'right_hip_x'], row[f'right_hip_y'])
    knee = Point(row[f'right_knee_x'], row[f'right_knee_y'])
    ankle = Point(row[f'right_ankle_x'], row[f'right_ankle_y'])
    return getAngle(ankle, knee, hip)


def computeLeftElbowAngle(row):
    wrist = Point(row[f'left_wrist_x'], row[f'left_wrist_y'])
    elbow = Point(row[f'left_elbow_x'], row[f'left_elbow_y'])
    shoulder = Point(row[f'left_shoulder_x'], row[f'left_shoulder_y'])
    return getAngle(wrist, elbow, shoulder)

def computeLeftShoulderAngle(row):
    elbow = Point(row[f'left_elbow_x'], row[f'left_elbow_y'])
    shoulder = Point(row[f'left_shoulder_x'], row[f'left_shoulder_y'])
    hip = Point(row[f'left_hip_x'], row[f'left_hip_y'])
    return getAngle(hip, shoulder, elbow)


def computeLeftKneeAngle(row):
    hip = Point(row[f'left_hip_x'], row[f'left_hip_y'])
    knee = Point(row[f'left_knee_x'], row[f'left_knee_y'])
    ankle = Point(row[f'left_ankle_x'], row[f'left_ankle_y'])
    return getAngle(ankle, knee, hip)

def computeBackAngle(row):
    bottom_of_back = Point((row[f'right_hip_x']+row[f'left_hip_x'])/2,
                           (row[f'right_hip_y']+row[f'left_hip_y'])/2)
    top_of_back = Point((row[f'right_shoulder_x']+row[f'left_shoulder_x'])/2,
                        (row[f'right_shoulder_y']+row[f'left_shoulder_y'])/2)
    top_of_frame_from_bottom_of_back = Point(
        (row[f'right_hip_x']+row[f'left_hip_x'])/2, 1)  # is 1 the correct max value here?
    return getAngle(bottom_of_back, top_of_back, top_of_frame_from_bottom_of_back)


# This will compute stride length at a given point in time
def computeStrideLength(row):
  left_ankle = Point(row[f'left_ankle_x'], row[f'left_ankle_y'])
  right_ankle = Point(row[f'right_ankle_x'], row[f'right_ankle_y'])

  # Calculate Euclidean distance
  stride_length_point_in_time = math.sqrt(math.pow((left_ankle.x - right_ankle.x),2) + math.pow((left_ankle.y - right_ankle.y),2))

  return stride_length_point_in_time

# Calculated to determine correct stride length for participant
# Choice of right leg is arbitrary
def computeRightLegLength(row):
  # left_hip = Point(row[f'left_hip_x'], row[f'left_hip_y'])
  right_hip = Point(row[f'right_hip_x'], row[f'right_hip_y'])
  # left_knee = Point(row[f'left_knee_x'], row[f'left_knee_y'])
  right_knee = Point(row[f'right_knee_x'], row[f'right_knee_y'])
  # left_ankle = Point(row[f'left_ankle_x'], row[f'left_ankle_y'])
  right_ankle = Point(row[f'right_ankle_x'], row[f'right_ankle_y'])

  upper_leg = math.sqrt(math.pow((right_hip.x - right_knee.x),2) + math.pow((right_hip.y - right_knee.y),2))
  lower_leg = math.sqrt(math.pow((right_ankle.x - right_knee.x),2) + math.pow((right_ankle.y - right_knee.y),2))

  leg_length = lower_leg + upper_leg
  return leg_length

def computeIdealStrideLength(row):
  leg_length = computeRightLegLength(row)
  return 0.4 * leg_length # TODO seems right but should back this up with some actual research

# TODO if time can add whether is ok, good, or great based on how far from ideal angle (e.g. 5 degrees is great, 10 is good, 15 is okay)
def isGoodElbowAngle(elbow_angle):
  # 90 degrees +/- 10 degrees
  # TODO what is the best range? 90 is definitely right
  if elbow_angle >= 80 and elbow_angle <= 100:
    return True
  return False

def isGoodKneeAngle(knee_angle):
  # 225 degrees +/- 10 degrees
  # TODO what is the best range? What is best angle?
  if knee_angle >= 215 and knee_angle <= 235:
    return True
  return False

def isGoodBackAngle(back_angle):
  # 185 degrees + 10 degrees or - 5 (since leaning forward is more ok than back)
  # TODO what is the best range? 90 is definitely right
  if back_angle >= 180 and back_angle <= 195:
    return True
  return False

def isStrideLength(stride_length, ideal_stride):
  # ideal_stride as calcualted from leg length, +/- .1 in picture pixels (this might have to be changed)
  # TODO what is the best range?
  if stride_length >= (ideal_stride - .1) and stride_length <= (ideal_stride + .1):
    return True
  return False

# TODO need to see if there is existing research on this - I took a quick glance and could not find anything
def isGoodPosture(row):
  stride_length = row['stride_length']
  ideal_stride = row['ideal_stride']

  right_elbow_angle = row['right_elbow_angle']
  # right_shoulder_angle = row['right_shoulder_angle']
  right_knee_angle = row['right_knee_angle']

  left_elbow_angle = row['left_elbow_angle']
  # left_shoulder_angle = row['left_shoulder_angle']
  left_knee_angle = row['left_knee_angle']

  back_angle = row['back_angle']

  # Calculate weighted metric on whether good posture or not
  # Amount added ranges from [0,1]. Higher added values indicates more importance for posture
  weighted_posture_metric = 0

  # TODO get rid of hardcoded weights - maybe have standardized low, medium, and high weight variables defined before this method?
  if isGoodElbowAngle(right_elbow_angle):
    weighted_posture_metric = weighted_posture_metric + 0.4
  if isGoodElbowAngle(left_elbow_angle):
    weighted_posture_metric = weighted_posture_metric + 0.4

  if isGoodKneeAngle(right_knee_angle):
    weighted_posture_metric = weighted_posture_metric + 0.8
  if isGoodKneeAngle(left_knee_angle):
    weighted_posture_metric = weighted_posture_metric + 0.8

  if isGoodBackAngle(back_angle):
    weighted_posture_metric = weighted_posture_metric + 0.8

  if isStrideLength(stride_length, ideal_stride):
    weighted_posture_metric = weighted_posture_metric + 0.9

  # Make call whether posture is good enough or not
  # TODO check if there is a method to this so it is less arbitrary
  # Currently highest possible total is 4.3
  # Probably missing two 0.8s is ok, so we'll say over 2.7 is good
  if weighted_posture_metric >= 2.7:
    return True
  return False 


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
    context = videointelligence.types.VideoContext(person_detection_config=config)

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

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )


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

    # TODO is Excel the right format?
    file_to_write = 'is_good_posture.xlsx'
    # Convert to Excel
    # TODO maybe just convert the is_good_posture column?
    excel_to_write = annotationsPd.to_excel(file_to_write)

    upload_blob("w251_test", file_to_write, file_to_write)

