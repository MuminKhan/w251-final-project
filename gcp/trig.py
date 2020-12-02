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
