import numpy as np
import time
import cv2
from ultralytics import YOLO

def ball_tracker(session):
    # NAO-Services
    motion = session.service("ALMotion")
    posture = session.service("ALRobotPosture")
    video_service = session.service("ALVideoDevice")

    motion.wakeUp()
    posture.goToPosture("StandInit", 0.5)

    # cam settings
    # 0=Top-Cam, 1=Bottom-Cam; Resolution=1: QVGA (320x240); Color=11: RGB
    resolution = 1
    color_space = 11
    fps = 15
    cam_name = "cam"
    cam = video_service.subscribeCamera(cam_name, 1, resolution, color_space, fps)

    model = YOLO("./yolo_model/best.pt")

    # ball cache
    last_seen = None
    lost_timeout = 1.5


    try:
        while True:
            image_data = video_service.getImageRemote(cam)
            if image_data is None:
                print("Kein Bild empfangen, warte ggf. kurz...")
                time.sleep(0.1)
                continue

            width, height = image_data[0], image_data[1]
            image = np.frombuffer(image_data[6], dtype=np.uint8).reshape((height, width, 3))

            # Bild anzeigen
            cv2.imshow("NAO Kamera", image)
            cv2.waitKey(1)

            # YOLO
            results = model(image)
            result = results[0]
            boxes = result.boxes

            current_time = time.time()
            ball_found = False

            if boxes is not None and len(boxes) > 0:
                box = boxes[0]
                xyxy = box.xyxy[0].cpu().numpy()
                x1, y1, x2, y2 = xyxy
                center_x = int((x1 + x2) / 2)
                center_y = int((y1 + y2) / 2)

                # caching
                last_seen = {
                    "center_x": center_x,
                    "center_y": center_y,
                    "timestamp": current_time
                }
                ball_found = True

            if ball_found:
                print(f"Ball gefunden bei x={center_x}, y={center_y}")
                diff_x = center_x - (width // 2)

            elif last_seen and (current_time - last_seen["timestamp"] < lost_timeout):
                diff_x = last_seen["center_x"] - (width // 2)
                print("Verwende gecachte Ballposition.")

            else:
                if last_seen:
                    if last_seen["center_x"] < (width // 2):
                        direction = "left"
                        motion.move(0, 0, 0.3)
                    else:
                        direction = "right"
                        motion.move(0, 0, -0.3)
                    print(f"Ball verloren – Suche durch Drehen nach {direction}.")
                else:
                    motion.move(0, 0, 0.3)
                    print("Ball nie gesehen – Standard-Drehung.")
                time.sleep(0.1)
                continue

            align_threshold = int(width * 0.30)  # 30%

            if abs(diff_x) > align_threshold:
                if diff_x < 0:
                    motion.move(0, 0, 0.2)
                    print("Drehe nach links")
                else:
                    motion.move(0, 0, -0.2)
                    print("Drehe nach rechts")
            else:
                motion.move(0.1, 0, 0)
                print("Geradeaus")


            time.sleep(0.1)

    except KeyboardInterrupt:
        print("Beendet durch Benutzer.")
    finally:
        motion.stopMove()
        cv2.destroyAllWindows()
        video_service.unsubscribe(cam_name)
        motion.rest()