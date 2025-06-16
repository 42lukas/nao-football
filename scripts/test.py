#!/usr/bin/env python3
import qi
import sys
import cv2
from dotenv import load_dotenv
import os
import numpy as np
import time
from wake_up import wake_up

load_dotenv()
IP_ADDRESS = os.getenv("IP_ADDRESS")

def main(robot_ip, robot_port):
    # 1. Session aufbauen
    session = qi.Session()
    try:
        session.connect("192.168.200.52:9559")
    except RuntimeError:
        print(f"Cannot connect to NAO at {robot_ip}:{robot_port}")
        sys.exit(1)

    wake_up(session)
    # 2. Video-Service holen
    cam = session.service("ALVideoDevice")
    motion = session.service("ALMotion")

    motion.setAngles("HeadPitch", 0.35, 0.2)

    # 3. Kamera abonnieren (0=Top-Cam, 1=Bottom-Cam; Resolution=2: 640x480; Color=11: BGR)
    resolution = 1      # kQVGA (320x240)=1, VGA (640x480)=2, HD (1280x960)=3
    color_space = 11    # kBGRColorSpace
    fps = 30
    camera_name = "camera"
    client_name = cam.subscribeCamera(camera_name, 1, resolution, color_space, fps)

    try:
        print("Starte Kamera-Stream. Drücke ESC zum Beenden.")
        while True:
            # 4. Bild abrufen
            frame = cam.getImageRemote(client_name)
            if frame is None:
                print("Kein Bild erhalten.")
                break

            # 5. Metadaten auspacken
            width = frame[0]
            height = frame[1]
            array = frame[6]  # Bilddaten als flache Liste
            # In NumPy-Array umwandeln und reshapen
            img = np.frombuffer(array, dtype=np.uint8).reshape((height, width, 3))

            # 6. Anzeige mit OpenCV
            cv2.imshow("NAO-Kamera", img)
            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # ESC
                break

            # kleine Pause, um CPU-Last zu senken
            time.sleep(0.01)

    finally:
        # 7. Aufräumen
        cam.unsubscribe(camera_name)
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main(IP_ADDRESS, 9559)