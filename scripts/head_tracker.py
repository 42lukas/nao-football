"""
head_tracker.py

Module to control NAO head movement to center a detected ball.
"""

# Gain factor: radians per pixel offset
MOVE_GAIN = 0.002

def control_head(motion, diff_x, diff_y, image_width, center_rect_ratio=0.1):
    """
    Adjust NAO head (yaw and pitch) to center the ball in the camera view.

    Args:
        motion: ALMotion service instance.
        diff_x: horizontal pixel difference between ball center and image center.
        diff_y: vertical pixel difference between ball center and image center.
        image_width: width of the camera image in pixels.
        center_rect_ratio: ratio of image width to define a deadzone around center.
    """
    center_rect_size = int(image_width * center_rect_ratio)
    # yaw adjustment (left/right)
    if abs(diff_x) > center_rect_size:
        yaw = motion.getAngles("HeadYaw", True)[0]
        target_yaw = float(yaw - diff_x * MOVE_GAIN)
        motion.setAngles("HeadYaw", target_yaw, 0.1)
    # pitch adjustment (up/down)
    if abs(diff_y) > center_rect_size:
        pitch = motion.getAngles("HeadPitch", True)[0]
        target_pitch = float(pitch - diff_y * MOVE_GAIN)
        motion.setAngles("HeadPitch", target_pitch, 0.1)
