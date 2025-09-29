import threading
from camera import main as camera_main
from test import main as test_main

if __name__ == "__main__":
    camera_thread = threading.Thread(target=camera_main)
    test_thread = threading.Thread(target=test_main)

    camera_thread.start()
    test_thread.start()

    camera_thread.join()
    test_thread.join()