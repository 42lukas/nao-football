import qi
import socket
import struct
import time
import os
import dotenv as env

env.load_dotenv()
IP_ADDRESS = os.getenv("IP_ADDRESS")
DEIN_PC_IP = os.getenv("DEIN_PC_IP")

def main():
    session = qi.Session()
    session.connect(f"tcp://{IP_ADDRESS}")  # oder interne IP

    video = session.service("ALVideoDevice")
    name = video.subscribeCamera("pic", 0, 1, 11, 5)  # 320x240 RGB, 5 FPS

    s = socket.socket()
    s.connect((DEIN_PC_IP, 5000))  # ← IP deines Rechners angeben

    while True:
        img = video.getImageRemote(name)
        if img:
            data = img[6]
            size = len(data)
            s.sendall(struct.pack("!I", size) + data)
        time.sleep(0.2)

if __name__ == "__main__":
    main()