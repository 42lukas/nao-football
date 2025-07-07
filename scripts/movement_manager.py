# thresholds for tracking
ALIGN_THRESHOLD_RATIO = 0.25
FORWARD_SPEED = 0.1           
ROTATE_SPEED = 0.2            

def move_towards_ball(motion, diff_x, image_width):
    """
    Rotate or move the robot towards the ball based on horizontal offset.

    Args:
        motion: ALMotion service instance.
        diff_x: horizontal pixel difference between ball center and image center.
        image_width: width of the camera image in pixels.
    """
    align_threshold = int(image_width * ALIGN_THRESHOLD_RATIO)
    if abs(diff_x) > align_threshold:
        # rotate in place to align
        if diff_x < 0:
            motion.move(0, 0, ROTATE_SPEED)
            print("Drehe nach links")
        else:
            motion.move(0, 0, -ROTATE_SPEED)
            print("Drehe nach rechts")
    else:
        # move forward towards the ball
        motion.move(FORWARD_SPEED, 0, 0)
        print("Laufe geradeaus")