import cv2

def list_cameras(max_index=100):
    for i in range(max_index):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            print(f"Camera found at index {i}")
            cap.release()
        else:
            cap.release()

list_cameras()
