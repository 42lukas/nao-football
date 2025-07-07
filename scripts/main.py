import qi
from wake_up import wake_up
from arms_behind_back import arms_behind_back
from ball_tracker import ball_tracker

def main():
    """
    Initialize robot and start autonomous ball tracking.
    """
    session = qi.Session()
    session.connect("tcp://192.168.200.52:9559")

    print("Starte autonomen Ball-Tracking-Modus...")
    wake_up(session)
    ball_tracker(session)

if __name__ == "__main__":
    main()