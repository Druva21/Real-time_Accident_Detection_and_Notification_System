import cv2
import numpy as np

def compute_motion_intensity(current_frame, previous_frame):
    if previous_frame is None or current_frame is None:
        return 0.0
    try:
        gray1 = cv2.cvtColor(previous_frame, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
        flow = cv2.calcOpticalFlowFarneback(gray1, gray2, None,
                                            0.5, 3, 15, 3, 5, 1.2, 0)
        mag, _ = cv2.cartToPolar(flow[..., 0], flow[..., 1])
        return float(np.mean(mag))
    except Exception as e:
        print("Optical flow error:", e)
        return 0.0
