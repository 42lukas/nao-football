# NAO-Plays-Soccer ⚽

This project aims to program a humanoid **NAO robot** that can play soccer.  
The control logic is combined with a **self-trained YOLO object detection model** to detect the ball.  

This repository contains a robot soccer project implemented in Python. It was developed as part of a university course at the HWR Berlin.

---

## Requirements ✅
- Robot must be programmed  
- Robot must be able to walk  
- Robot must be able to detect the ball  
- Robot must be able to kick the ball without losing balance  

---

## Get Started 🚀

To begin programming the NAO robot, you need to install the **NAOqi Framework**.  
It is **recommended to use Linux** in order to work with modern Python versions (≥ 3.x).

### Installation
Install the required Python package with:

```bash
pip install qi
```
### Example Code
```python
import qi

# Connect to the robot (replace with your NAO's IP address)
session = qi.Session()
session.connect("tcp://192.168.1.10:9559")

# Use the text-to-speech service
tts = session.service("AlTextToSpeech")
tts.say("Hi, I am NAO!")

```

---

## Project Structure 📂
```text
scripts/
│
├── main.py
├── test.py
├── arms_behind_back.py
├── kick.py
├── wake_up.py
├── ball_tracker.py
│
└── camera/        # Camera modules
    ├── main.py
    ├── test.py
    ├── camera.py


Yolo-Model/
└── best.pt        # Trained YOLO model

````
## Run the Project ▶️

Execute the main script with:

```bash
python scripts/main.py
```
## Used Technologies🤖
- Python: Python 3.12.2
- Object detection: YOLOv5
- NAO6
- GitHub

## Contributors 👥
- Nasser
- Lukas
- Sinan
- Mihoshi
