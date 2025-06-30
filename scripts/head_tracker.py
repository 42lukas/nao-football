import qi
import cv2
import numpy as np
import dotenv as env
import os
import time

env.load_dotenv()
IP_ADDRESS = os.getenv("IP_ADDRESS")

CENTER_RECT_SIZE = 60  # half size of the rectangle where the ball is considered centered
MOVE_GAIN = 0.002       # radian per pixel for head adjustment


def get_ball_position(image):
    """Return the (x, y) position of the largest orange object in the image."""
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_orange = np.array([5, 150, 150])
    upper_orange = np.array([15, 255, 255])
    mask = cv2.inRange(hsv, lower_orange, upper_orange)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None
    largest = max(contours, key=cv2.contourArea)
    (x, y), radius = cv2.minEnclosingCircle(largest)
    if radius < 5:
        return None
    return int(x), int(y)


def track_ball():
    session = qi.Session()
    session.connect(f"tcp://{IP_ADDRESS}")

    cam = session.service("ALVideoDevice")
    motion = session.service("ALMotion")

    resolution = 2      # 640x480
    color_space = 11    # BGR
    fps = 15
    client_name = cam.subscribeCamera("ballTracker", 0, resolution, color_space, fps)

    try:
        width = 640
        height = 480
        center_x = width // 2
        center_y = height // 2
        while True:
            frame = cam.getImageRemote(client_name)
            if frame is None:
                continue
            width = frame[0]
            height = frame[1]
            img = np.frombuffer(frame[6], dtype=np.uint8).reshape((height, width, 3))

            pos = get_ball_position(img)
            if pos is not None:
                x, y = pos
                dx = x - center_x
                dy = y - center_y
                if abs(dx) > CENTER_RECT_SIZE:
                    yaw = motion.getAngles("HeadYaw", True)[0]
                    motion.setAngles("HeadYaw", yaw - dx * MOVE_GAIN, 0.1)
                if abs(dy) > CENTER_RECT_SIZE:
                    pitch = motion.getAngles("HeadPitch", True)[0]
                    motion.setAngles("HeadPitch", pitch - dy * MOVE_GAIN, 0.1)
            time.sleep(0.05)
    finally:
        cam.unsubscribe(client_name)


if __name__ == "__main__":
    track_ball()
