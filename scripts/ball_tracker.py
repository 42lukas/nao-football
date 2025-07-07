import numpy as np
import time
import cv2
import math
from ultralytics import YOLO
from kick import kick
from wake_up import wake_up
from head_tracker import control_head
from movement_manager import move_towards_ball

# camera settings
RESOLUTION = 1    # 320×240 for performance
COLOR_SPACE = 11  # RGB
FPS = 15
CAM_NAME = "ffg"

# thresholds and speeds
ALIGN_THRESHOLD_RATIO = 0.25
FORWARD_SPEED = 0.1
ROTATE_SPEED = 0.2

# camera parameter IDs
BRIGHTNESS_ID = 0

# timeouts
SWITCH_DELAY = 1.0
LOST_TIMEOUT = 1.5


def ball_tracker(session):
    motion = session.service("ALMotion")
    video_service = session.service("ALVideoDevice")

    model = YOLO("./yolo_model/best.pt")

    # State variables
    current_cam = 1  # bottom cam
    last_seen = None
    start_time = time.time()
    switch_time = None
    search_mode = False

    # Subscribe camera
    cam_handle = video_service.subscribeCamera(
        CAM_NAME, current_cam, RESOLUTION, COLOR_SPACE, FPS
    )
    # Manual camera parameters
    video_service.setParameter(current_cam, BRIGHTNESS_ID, 180)

    try:
        while True:
            now = time.time()
            data = video_service.getImageRemote(cam_handle)
            if data is None:
                time.sleep(0.1)
                continue
            w, h = data[0], data[1]
            img = np.frombuffer(data[6], dtype=np.uint8).reshape((h, w, 3))

            # Live Preview
            cv2.imshow("NAO View", img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            # Detection only if not in search_mode
            if not search_mode:
                res = model(img)[0]
                boxes = res.boxes.xyxy
                ball_found = len(boxes) > 0
                cx = cy = None
                if ball_found:
                    x1, y1, x2, y2 = boxes[0].cpu().numpy()
                    cx = int((x1 + x2) / 2)
                    cy = int((y1 + y2) / 2)
                    last_seen = {"cx": cx, "cy": cy, "time": now}
                    # reset camera/timers
                    start_time = now
                    switch_time = None
                else:
                    # if never seen, maybe switch camera
                    if last_seen is None and switch_time is None and now - start_time > SWITCH_DELAY and current_cam == 1:
                        video_service.unsubscribe(cam_handle)
                        current_cam = 0
                        cam_handle = video_service.subscribeCamera(
                            CAM_NAME, current_cam, RESOLUTION, COLOR_SPACE, FPS
                        )
                        switch_time = now
                        continue
                    # if switched and still not found -> enter search
                    if current_cam == 0 and switch_time and not search_mode:
                        search_mode = True
                        print("Starte Suchverhalten...")

                # if ball found or cached within LOST_TIMEOUT
                if ball_found:
                    cx_use, cy_use = cx, cy
                elif last_seen and now - last_seen["time"] < LOST_TIMEOUT:
                    cx_use, cy_use = last_seen["cx"], last_seen["cy"]
                else:
                    # neither found nor recently seen
                    if not search_mode:
                        continue
                    cx_use = cy_use = None

            # Search behaviour: rotate and bob head
            if search_mode:
                motion.move(0, 0, ROTATE_SPEED)
                elapsed = now - switch_time
                pitch = 0.3 * math.sin(2 * math.pi * 0.5 * elapsed)
                motion.setAngles("HeadPitch", float(pitch), 0.1)
                continue

            offset_x = cx_use - (w // 2)
            offset_y = cy_use - (h // 2)

            # Control head & body
            control_head(motion, offset_x, offset_y, w)
            move_towards_ball(motion, offset_x, w)

            time.sleep(0.1)

    except KeyboardInterrupt:
        print("Abgebrochen")
    finally:
        video_service.unsubscribe(cam_handle)
        motion.stopMove()
        cv2.destroyAllWindows()
        motion.rest()