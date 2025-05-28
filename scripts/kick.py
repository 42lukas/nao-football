# coding: utf-8
import time
import wake_up

def kick(session, leg="left"):
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

    # Gewicht auf Standbein
    motion_service.setFootStepsWithSpeed([support_leg], [[0.0, 0.0, 0.0]], [0.3], False)
    time.sleep(1.0)

    # Kick-Pfad in 3 Schritten:
    path = [
        [0.00, 0.00, 0.5, 0.0, 0.0, 0.0],   # 1. anheben (5 cm nach oben)
        [0.10, 0.00, 0.05, 0.5, 0.0, 0.0],   # 2. nach vorn schwingen (10 cm)
        [0.00, 0.00, 0.00, 0.0, 0.0, 0.0]    # 3. zurück auf Boden
    ]
    times = [0.4, 0.8, 1.2]
    axis_mask = 63  # alle DOFs
    space = motion_service.SPACE_TORSO

    motion_service.positionInterpolation(
        effector, space, path, axis_mask, times, False
    )

    time.sleep(0.5)
    posture_service.goToPosture("StandInit", 0.5)