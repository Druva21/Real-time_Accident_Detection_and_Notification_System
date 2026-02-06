import cv2
from tkinter import filedialog, messagebox

def get_camera_capture():
    backends = [cv2.CAP_DSHOW, cv2.CAP_MSMF, cv2.CAP_V4L2, cv2.CAP_ANY]
    for b in backends:
        try:
            cap = cv2.VideoCapture(0, b)
            if cap.isOpened():
                return cap
            cap.release()
        except Exception:
            continue
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        messagebox.showerror("Camera Error", "Could not open camera. Make sure it's not used by another app and permissions are allowed.")
        return None
    return cap

def get_video_capture_from_file():
    file = filedialog.askopenfilename(title="Select Video",
                                      filetypes=[("Video files", "*.mp4;*.avi;*.mov;*.mkv")])
    if not file:
        return None
    cap = cv2.VideoCapture(file)
    if not cap.isOpened():
        messagebox.showerror("Video Error", "Could not open selected video.")
        return None
    return cap
