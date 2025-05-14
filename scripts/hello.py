import qi
import dotenv as env 
import os

env.load_dotenv()
IP_ADDRESS = os.getenv("IP_ADDRESS")

def main():
    session = qi.Session()
    session.connect(f"tcp://{IP_ADDRESS}")  # IP deines NAO
    tts = session.service("ALTextToSpeech")
    tts.say("Hallo vom Team!") 

    motion = session.service("ALMotion")

    posture = session.service("ALRobotPosture")
    posture.goToPosture("StandInit", 0.5)

    motion.moveInit()
    # (gerade, quer, drehen)
    motion.moveTo(0.2, 0, 0) 
    motion.moveTo(0, 0.2, 0)
    motion.moveTo(0, 0, 1)
    motion.moveTo(0, 0, -1)
    motion.moveTo(0, -0.2, 0)
    motion.moveTo(-0.2, 0, 0)



if __name__ == "__main__":
    main()

