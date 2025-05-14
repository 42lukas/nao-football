#!/usr/bin/env python3
import qi
import argparse
import sys
import cv2
import dotenv as env
import numpy as np
import time

env.load_dotenv()
IP_ADDRESS = env.get_key("IP_ADDRESS")

def main(robot_ip, robot_port):
    # 1. Session aufbauen
    session = qi.Session()
    try:
        session.connect(f"{IP_ADDRESS}:{robot_port}")
    except RuntimeError:
        print(f"Cannot connect to NAO at {robot_ip}:{robot_port}")
        sys.exit(1)

    # 2. Video-Service holen
    cam = session.service("ALVideoDevice")

    # 3. Kamera abonnieren (0=Top-Cam, 1=Bottom-Cam; Resolution=2: 640x480; Color=11: BGR)
    resolution = 2      # kQVGA (320x240)=1, VGA (640x480)=2, HD (1280x960)=3
    color_space = 11    # kBGRColorSpace
    fps = 15
    client_name = cam.subscribeCamera("camClient", 0, resolution, color_space, fps)

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
        cam.unsubscribe(client_name)
        cv2.destroyAllWindows()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Zeige den NAO-Kamera-Stream auf dem PC")
    parser.add_argument("--ip", type=str, required=True,
                        help="IP-Adresse des NAO (z. B. 169.254.119.143)")
    parser.add_argument("--port", type=int, default=9559,
                        help="Port des NAO (Standard 9559)")
    args = parser.parse_args()
    main(args.ip, args.port)