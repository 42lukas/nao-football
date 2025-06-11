def wake_up(session):
    """Wake up the robot and set it to a standing posture.
    Args:
        session (qi.Session): The session to connect to the robot.
    """
    posture = session.service("ALRobotPosture")
    posture.goToPosture("StandInit", 0.5)

if __name__ == "__main__":
    wake_up()