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

    # 2. Posture-Service holen
    posture = session.service("ALRobotPosture")
    # Aufstehen
    posture.goToPosture("StandInit", 0.5)
    time.sleep(2)
    # Hinsetzen
    posture.goToPosture("Sit", 0.5)
    posture.goToPosture("StandInit", 0.5)

if __name__ == "__main__":
    main()