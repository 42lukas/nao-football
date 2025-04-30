import qi

def main():
    session = qi.Session()
    session.connect("169.254.119.143")  # IP deines NAO
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

