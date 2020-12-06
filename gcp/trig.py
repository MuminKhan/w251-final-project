# Source: https://github.com/google/making_with_ml/blob/master/sports_ai/Sports_AI_Analysis.ipynb

import math


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
    stride_length_point_in_time = math.sqrt(math.pow(
        (left_ankle.x - right_ankle.x), 2) + math.pow((left_ankle.y - right_ankle.y), 2))

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

    upper_leg = math.sqrt(math.pow(
        (right_hip.x - right_knee.x), 2) + math.pow((right_hip.y - right_knee.y), 2))
    lower_leg = math.sqrt(math.pow(
        (right_ankle.x - right_knee.x), 2) + math.pow((right_ankle.y - right_knee.y), 2))

    leg_length = lower_leg + upper_leg
    return leg_length


def computeIdealStrideLength(row):
    leg_length = computeRightLegLength(row)
    # TODO seems right but should back this up with some actual research
    return 0.4 * leg_length

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
