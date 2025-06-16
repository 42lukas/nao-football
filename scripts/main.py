import qi
from kick import kick
from arms_behind_back import arms_behind_back
from wake_up import wake_up
from ball_tracker import ball_tracker

session = qi.Session()
session.connect("tcp://192.168.200.52:9559")   # NAO-IP und Port