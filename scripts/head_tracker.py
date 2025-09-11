import os
import time

import cv2
import numpy as np
import qi
import torch
from dotenv import load_dotenv

load_dotenv()
IP_ADDRESS = os.getenv("IP_ADDRESS")
MODEL_PATH = os.getenv("BALL_MODEL_PATH", "ball_detector.pt")

# half-size of rectangle where the ball is considered centered (pixels)
CENTER_RECT_SIZE = 60
# radian per pixel for head adjustment
MOVE_GAIN = 0.002


def load_model(path: str):
    """Load the torchscript model for ball detection."""
    model = torch.jit.load(path, map_location="cpu")
    model.eval()
    return model


def get_ball_position(model, image: np.ndarray):
    """Return ball center (x, y) using the provided detection model."""
    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    tensor = torch.from_numpy(img).permute(2, 0, 1).float() / 255.0
    tensor = tensor.unsqueeze(0)
    with torch.no_grad():
        output = model(tensor)
    if isinstance(output, (list, tuple)):
        output = output[0]
    if output is None or len(output) == 0:
        return None
    box = output[0]
    x = (box[0] + box[2]) / 2
    y = (box[1] + box[3]) / 2
    return int(x), int(y)


def track_ball(model_path: str = MODEL_PATH):
    model = load_model(model_path)
    session = qi.Session()
    session.connect(f"tcp://{IP_ADDRESS}")

    cam = session.service("ALVideoDevice")
    motion = session.service("ALMotion")

    resolution = 2
    color_space = 11
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

            pos = get_ball_position(model, img)
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
