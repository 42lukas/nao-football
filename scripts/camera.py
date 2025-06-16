#!/usr/bin/env python3
import qi
import sys
import cv2
import dotenv as env
import numpy as np
import time
import os

env.load_dotenv()
IP_ADDRESS = os.getenv("IP_ADDRESS")
ROBOT_PORT = os.getenv("ROBOT_PORT") 

def main():
    # 1. Session aufbauen
    session = qi.Session()
    try:
        session.connect(f"tcp://{IP_ADDRESS}:{ROBOT_PORT}")
    except RuntimeError:
        print(f"Cannot connect to NAO at {IP_ADDRESS}:{ROBOT_PORT}")
        sys.exit(1)

    # 2. Video-Service holen
    cam = session.service("ALVideoDevice")

    # 3. Kamera abonnieren
    resolution = 2      # VGA (640x480)
    color_space = 11    # kBGRColorSpace
    fps = 30
    client_name = cam.subscribeCamera("camClient", 0, resolution, color_space, fps)

    try:
        print("Starte Kamera-Stream. Drücke ESC zum Beenden.")
        while True:
            frame = cam.getImageRemote(client_name)
            if frame is None:
                print("Kein Bild erhalten.")
                break

            width = frame[0]
            height = frame[1]
            array = frame[6]
            img = np.frombuffer(array, dtype=np.uint8).reshape((height, width, 3))

            cv2.imshow("NAO-Kamera", img)
            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # ESC
                break

            time.sleep(0.01)

    finally:
        cam.unsubscribe(client_name)
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
