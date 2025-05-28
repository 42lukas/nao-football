# coding: utf-8
import time
import wake_up

FRAME_TORSO = 0

def kick(session, leg):
    motion_service = session.service("ALMotion")
    posture_service = session.service("ALRobotPosture")

    # Aufstehen und Grundhaltung
    wake_up.wake_up(session)

    if leg.lower() == "left":
        effector = "LLeg"
        support_leg = "RLeg"
    elif leg.lower() == "right":
        effector = "RLeg"
        support_leg = "LLeg"
    else:
        raise ValueError("Ungueltiges Bein. Verwende 'left' oder 'right'.")

    # Statt nur 5cm auf das Support-Leg -> mehr Abstand, um Gewichtsverlagerung zu erzwingen
    motion_service.setFootStepsWithSpeed(
        [support_leg],
        [[0.0, 0.07, 0.0]],  # Seitlich mehr verlagern
        [0.5],
        False
    )
    time.sleep(0.5)

   

    # Kickpfad relativ zur aktuellen Position
    path = [
        [0.0, 0.0, 0.02, 0.0, 0.0, 0.0],
        [0.08, 0.0, 0.02, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    ]
    times = [0.1, 0.4, 0.9]
    axis_mask = 63  # alle DOFs

    print("→ Kickbewegung startet...")
    motion_service.positionInterpolation(
        effector, FRAME_TORSO, path, axis_mask, times, False
    )
    print("→ Kick beendet.")

    time.sleep(0.5)
    posture_service.goToPosture("StandInit", 0.5)