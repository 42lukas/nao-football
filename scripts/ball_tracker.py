import qi
import cv2
import numpy as np
from ultralytics import YOLO


def main():
    session = qi.Session()
    try:
        session.connect("tcp://192.168.200.55:9559")
    except RuntimeError:
        print("Verbindung zum NAO fehlgeschlagen.")
        return
    motion = session.service("ALMotion")
    posture = session.service("ALRobotPosture")

    posture.goToPosture("StandInit", 0.5)
    motion.wakeUp()

    video_service = session.service("ALVideoDevice")
    tts = session.service("ALTextToSpeech")
    motion = session.service("ALMotion")
    posture = session.service("ALRobotPosture")

    tts.say("Starting Tracker")

    
    #letze zahl fps, erste kamera
    name_id = video_service.subscribeCamera("nao_cam", 1, 1, 11, 10)

    # Lade YOLO Modell
    model = YOLO("./yolo_model/best.pt")  

    # Anfangswerte für Kopfposition (oben nach dem Modell-Laden einfügen)
    head_yaw = 0.0
    head_pitch = 0.0


    try:
        while True:
            image = video_service.getImageRemote(name_id)
            if image is None:
                print("Kein Bild erhalten.")
                continue

            width, height, array = image[0], image[1], image[6]
            frame = np.frombuffer(array, dtype=np.uint8).reshape((height, width, 3))
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            # YOLO-Inferenz
            results = model.track(source=frame, persist=True, conf=0.5, verbose=False)

                        # Kopf-Tracking
            for result in results:
                for box in result.boxes:
                    cls_id = int(box.cls[0])
                    cls_name = model.names[cls_id]

                    if cls_name.lower() == "ball":
                        x1, y1, x2, y2 = map(int, box.xyxy[0])  # Bounding Box
                        cx = (x1 + x2) // 2
                        cy = (y1 + y2) // 2

                        # Mittelpunkt der Kamera
                        center_x = width // 2
                        center_y = height // 2

                        # Unterschied zum Bildzentrum
                        dx = cx - center_x
                        dy = cy - center_y

                        # Skalierungsfaktor (anpassen je nach Reaktion)
                        sensitivity_x = 0.002
                        sensitivity_y = 0.002

                        # Berechne neue Kopfposition
                        head_yaw -= dx * sensitivity_x
                        head_pitch += dy * sensitivity_y

                        # Begrenze Bewegungsbereich (Werte in Radiant)
                        head_yaw = max(-1.5, min(1.5, head_yaw))
                        head_pitch = max(-0.5, min(0.5, head_pitch))

                        # Bewege Kopf
                        motion.setAngles(["HeadYaw", "HeadPitch"], [head_yaw, head_pitch], 0.2)

                        max_deviation = 30  # Pixelabweichung, bevor Bewegung nötig ist

                        if abs(dx) > max_deviation:
                            angle = -dx * 0.002  # Drehrichtung gegensätzlich
                            angle = max(-0.5, min(0.5, angle))  # begrenzen auf -0.5 bis 0.5 rad
                            motion.moveTo(0, 0, angle)

                        break  


            annotated_frame = results[0].plot()

            cv2.imshow("NAO + YOLO", annotated_frame)

            # Beenden mit Taste 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        video_service.unsubscribe(name_id)
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
