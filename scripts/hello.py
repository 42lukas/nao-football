import qi

def main():
    session = qi.Session()
    session.connect("169.254.210.161")  # IP deines NAO
    tts = session.service("ALTextToSpeech")
    tts.say("Hallo vom Team!")

if __name__ == "__main__":
    main()