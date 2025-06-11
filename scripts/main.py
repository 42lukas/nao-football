import qi
from kick import kick

session = qi.Session()
session.connect("tcp://192.168.200.52:9559")   # NAO-IP und Port

# Rechter Schuss:
kick(session, "right")