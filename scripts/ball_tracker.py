import qi
import cv2
import numpy as np
from ultralytics import YOLO


def main():
    session = qi.Session()
    try:
        session.connect("tcp://192.168.200.59:9559")
    except RuntimeError:
        print("Verbindung zum NAO fehlgeschlagen.")
        return

    # NAO-Services
    motion = session.service("ALMotion")
    posture = session.service("ALRobotPosture")
    video_service = session.service("ALVideoDevice")
    tts = session.service("ALTextToSpeech")

    # Initialisierung
    posture.goToPosture("StandInit", 0.5)
    motion.wakeUp()
    tts.say("Starting Tracker")

    # Kamera abonnieren: Bodenkamera, QVGA, RGB
    name_id = video_service.subscribeCamera("nao_cam", 1, 1, 11, 10)

    # YOLOv8 Modell laden
    model = YOLO("./yolo_model/best.pt")  

    head_yaw = 0.0
    head_pitch = 0.0
    frame_count = 0
    last_results = None

    try:
        while True:
            image = video_service.getImageRemote(name_id)
            if image is None:
                continue

            width, height, array = image[0], image[1], image[6]
            frame = np.frombuffer(array, dtype=np.uint8).reshape((height, width, 3))
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            # YOLO-Inferenz nur alle 3 Frames
            if frame_count % 5 == 0:
                results = model.track(source=frame, persist=True, conf=0.5, verbose=False)
                last_results = results
            else:
                results = last_results

            # Kopf-Tracking
            if results:
                for result in results:
                    for box in result.boxes:
                        cls_id = int(box.cls[0])
                        cls_name = model.names[cls_id]

                        if cls_name.lower() == "ball":
                            x1, y1, x2, y2 = map(int, box.xyxy[0])
                            cx = (x1 + x2) // 2
                            cy = (y1 + y2) // 2

                            center_x = width // 2
                            center_y = height // 2
                            dx = cx - center_x
                            dy = cy - center_y

                            sensitivity_x = 0.002
                            sensitivity_y = 0.002

                            head_yaw -= dx * sensitivity_x
                            head_pitch += dy * sensitivity_y

                            head_yaw = max(-1.5, min(1.5, head_yaw))
                            head_pitch = max(-0.5, min(0.5, head_pitch))

                            motion.setAngles(["HeadYaw", "HeadPitch"], [head_yaw, head_pitch], 0.2)

                            if abs(dx) > 30:
                                angle = -dx * 0.002
                                angle = max(-0.5, min(0.5, angle))
                                try:
                                    motion.moveTo(0, 0, float(angle))
                                except RuntimeError as e:
                                    print("Bewegung fehlgeschlagen:", e)

                            break

            # Bild anzeigen
            annotated_frame = frame if results is None else results[0].plot()
            cv2.imshow("NAO + YOLO", annotated_frame)

            frame_count += 1
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        try:
            video_service.unsubscribe(name_id)
        except Exception as e:
            print("Fehler beim Unsubscribe:", e)

        cv2.destroyAllWindows()
        tts.say("Tracker beendet")


if __name__ == "__main__":
    main()
