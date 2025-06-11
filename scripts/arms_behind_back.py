# coding: utf-8

def arms_behind_back(session):
    motion_service = session.service("ALMotion")
    posture_service = session.service("ALRobotPosture")

    posture_service.goToPosture("StandInit", 0.5)

    joint_names = [
        "LShoulderPitch", "LShoulderRoll", "LElbowRoll",
        "RShoulderPitch", "RShoulderRoll", "RElbowRoll"
    ]

    # Werte für gestreckte Arme nach hinten
    joint_angles = [
        2.1,  -2.0, -0.01,   # linker Arm
        2.1,  2.0,  0.01    # rechter Arm
    ]

    motion_service.angleInterpolation(joint_names, joint_angles, [1.0] * len(joint_names), True)