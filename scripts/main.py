import qi
from ball_tracker import ball_tracker

session = qi.Session()
session.connect("tcp://192.168.200.52:9559")

ball_tracker(session) # start ball tracker