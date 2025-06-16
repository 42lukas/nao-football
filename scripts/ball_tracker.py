import numpy as np
import time
import cv2
from ultralytics import YOLO

def ball_tracker(session):
    # NAO-Services
    motion = session.service("ALMotion")
    posture = session.service("ALRobotPosture")
    video_service = session.service("ALVideoDevice")
    tts = session.service("ALTextToSpeech")

    # Initialisierung
    motion.wakeUp()
    posture.goToPosture("StandInit", 0.5)
    tts.say("Start.")

    # Kamera abonnieren
    resolution = 1  # VGA
    color_space = 11  # RGB
    fps = 15
    cam_name = "BallTracker"
    cam = video_service.subscribeCamera("camClient", 1, resolution, color_space, fps)

    # YOLOv5-Modell laden
    model_path = "./yolo_model/best.pt"
    model = YOLO(model_path)

    try:
        while True:
            # Bild holen
            image_data = video_service.getImageRemote(cam)
            if image_data is None:
                print("Kein Bild empfangen, warte kurz...")
                time.sleep(0.1)
                continue
            
            print("Bild empfangen")

            width = image_data[0]
            height = image_data[1]
            array = image_data[6]
            image = np.frombuffer(array, dtype=np.uint8).reshape((height, width, 3))

            # YOLO-Inferenz
            results = model(image)
            cv2.imshow("NAO Kamera", image)
            cv2.waitKey(1)
            result = results[0]  # Nur ein Bild
            boxes = result.boxes  # Boxes-Objekt

            if boxes is not None and len(boxes) > 0:
                # Nur den ersten Ball nehmen
                box = boxes[0]
                xyxy = box.xyxy[0].cpu().numpy()
                x1, y1, x2, y2 = xyxy
                center_x = int((x1 + x2) / 2)
                center_y = int((y1 + y2) / 2)

                # Bildmitte und Steuerung
                img_center_x = image.shape[1] // 2
                diff_x = center_x - img_center_x

                if abs(diff_x) < 30:
                    motion.move(0.1, 0, 0)  # Geradeaus
                elif diff_x < 0:
                    motion.move(0, 0, 0.2)  # Links drehen
                else:
                    motion.move(0, 0, -0.2)  # Rechts drehen

                print(f"Ball gefunden bei x={center_x}, y={center_y}")
            else:
                motion.move(0, 0, 0.3)
                time.sleep(0.1)

            time.sleep(0.1)

    except KeyboardInterrupt:
        print("Beendet durch Benutzer.")
    finally:
        motion.stopMove()
        cv2.destroyAllWindows()
        video_service.unsubscribe(cam_name)
        motion.rest()