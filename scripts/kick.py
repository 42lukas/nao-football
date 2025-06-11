# coding: utf-8
import time

FRAME_TORSO = 0
AXIS_MASK_ALL = 63

def kick(session, leg):
    motion_service = session.service("ALMotion")
    posture_service = session.service("ALRobotPosture")

    # balance preparation
    effector_torso = "Torso"
    duration = 0.5
    current = motion_service.getPosition(effector_torso, FRAME_TORSO, True)
    target = current[:]

    if leg.lower() == "left":
        effector_leg = "LLeg"
        target[1] -= 0.0058
    elif leg.lower() == "right":
        effector_leg = "RLeg"
        target[1] += 0.0058
    else:
        raise ValueError("Ungueltiges Bein. Verwende 'left' oder 'right'.")

    motion_service.positionInterpolations(
        [effector_torso],
        FRAME_TORSO,
        [target],
        AXIS_MASK_ALL,
        duration,
        True
    )

    # kick
    path = [
        [0.0, 0.0, 0.03, 0.0, 0.0, 0.0],
        [0.05, 0.0, 0.03, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    ]
    times = [0.2, 0.4, 0.6]
    

    print("→ Kickbewegung startet...")
    motion_service.positionInterpolation(
        effector_leg, FRAME_TORSO, path, AXIS_MASK_ALL, times, False
    )
    print("→ Kick beendet.")

    time.sleep(0.5)
    posture_service.goToPosture("StandInit", 0.5)