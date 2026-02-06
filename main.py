"""
Accident Detection System (Enhanced GUI)
----------------------------------------
YOLOv8 + motion analysis + alert system.
"""

import cv2
import numpy as np
import time
import threading
from datetime import datetime
from ultralytics import YOLO
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# ===============================
# Configuration
# ===============================
MODEL_PATH = "models/auto_trained_model3/weights/best.pt"
CONFIDENCE_THRESHOLD = 0.6
MOTION_THRESHOLD = 0.97
ACCIDENT_COOLDOWN = 7  

# ===============================
# Accident Detection Core
# ===============================
class AccidentDetector:
    def __init__(self, video_source):
        self.video_source = video_source
        self.model = YOLO(MODEL_PATH)
        print(f"✅ Model loaded: {MODEL_PATH}")
        self.accident_detected = False
        self.last_accident_time = 0

    def detect_motion(self, frame1, frame2):
        gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        diff = cv2.absdiff(gray1, gray2)
        non_zero_count = np.count_nonzero(diff)
        total_pixels = diff.size
        motion_score = 1 - (non_zero_count / total_pixels)
        return motion_score

    def analyze(self):
        cap = cv2.VideoCapture(self.video_source)
        if not cap.isOpened():
            print("❌ Cannot open video source.")
            return

        ret, prev_frame = cap.read()
        if not ret:
            print("❌ Cannot read first frame.")
            return

        print("🎥 Accident detection started...")
        while True:
            ret, frame = cap.read()
            if not ret:
                print("⚠️ End of stream or error reading frame.")
                break

            # Run YOLOv8 inference
            results = self.model(frame)
            detections = results[0].boxes
            accident_confidence = 0

            for box in detections:
                conf = float(box.conf)
                cls = int(box.cls)
                if conf > CONFIDENCE_THRESHOLD:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    label = self.model.names[cls]
                    color = (0, 255, 0)
                    if "accident" in label.lower():
                        color = (0, 0, 255)
                        accident_confidence = max(accident_confidence, conf)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                    cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

            # Motion detection
            motion_score = self.detect_motion(prev_frame, frame)
            prev_frame = frame.copy()

            # Accident logic
            current_time = time.time()
            if (
                accident_confidence > CONFIDENCE_THRESHOLD
                and motion_score < MOTION_THRESHOLD
                and (current_time - self.last_accident_time) > ACCIDENT_COOLDOWN
            ):
                self.accident_detected = True
                self.last_accident_time = current_time
                print(f"🚨 Accident Detected! Confidence={accident_confidence:.2f}, Motion={motion_score:.3f}")
                threading.Thread(target=self.show_alert_popup).start()

            if self.accident_detected:
                cv2.putText(frame, "🚨 ACCIDENT DETECTED 🚨", (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)

            # Display frame
            cv2.imshow("Accident Detection", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("👋 Exiting...")
                break

        cap.release()
        cv2.destroyAllWindows()

    def show_alert_popup(self):
        alert = tk.Tk()
        alert.withdraw()
        messagebox.showwarning("Accident Detected!", "🚨 Accident detected! Please check the scene immediately.")
        alert.destroy()

# ===============================
# GUI Application
# ===============================
class AccidentDetectorApp:
    def __init__(self, master):
        self.master = master
        master.title("Accident Detection System")
        master.geometry("500x400")
        master.configure(bg="#0B132B")

        title = tk.Label(master, text="🚗 Accident Detection System 🚨",
                         font=("Arial", 18, "bold"), fg="#00D1FF", bg="#0B132B")
        title.pack(pady=30)

        subtitle = tk.Label(master, text="Choose Input Source",
                            font=("Arial", 13), fg="white", bg="#0B132B")
        subtitle.pack(pady=10)

        # Buttons styled
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=("Arial", 13, "bold"), padding=10)

        self.btn_camera = ttk.Button(master, text="📷 Use Camera", command=self.use_camera)
        self.btn_camera.pack(pady=10)

        self.btn_video = ttk.Button(master, text="🎞 Upload Video", command=self.upload_video)
        self.btn_video.pack(pady=10)

        ttk.Separator(master, orient="horizontal").pack(fill="x", pady=20)

        self.btn_exit = ttk.Button(master, text="❌ Exit", command=master.quit)
        self.btn_exit.pack(pady=10)

        footer = tk.Label(master, text="Developed by Druva Kumar | IIIT Kottayam",
                          font=("Arial", 10, "italic"), fg="#A9A9A9", bg="#0B132B")
        footer.pack(side="bottom", pady=20)

    def use_camera(self):
        self.master.destroy()
        detector = AccidentDetector(0)
        detector.analyze()

    def upload_video(self):
        path = filedialog.askopenfilename(
            title="Select a video file",
            filetypes=[("Video Files", "*.mp4 *.avi *.mov *.mkv")]
        )
        if path:
            self.master.destroy()
            detector = AccidentDetector(path)
            detector.analyze()
        else:
            messagebox.showinfo("Info", "No video selected!")

# ===============================
# Run
# ===============================
if __name__ == "__main__":
    root = tk.Tk()
    app = AccidentDetectorApp(root)
    root.mainloop()
