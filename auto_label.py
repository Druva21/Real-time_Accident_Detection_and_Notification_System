#!/usr/bin/env python3
"""
auto_label.py
-------------
Automatically labels frames from videos in 'accident_videos/' using a pretrained YOLO model.
Generates YOLO-format annotations (.txt) for quick correction in LabelImg.
"""

import os
import cv2
from ultralytics import YOLO
import numpy as np
from pathlib import Path
from tqdm import tqdm

# Paths
BASE_DIR = Path(__file__).resolve().parent
VIDEO_DIR = BASE_DIR / "accident_videos"
IMAGE_DIR = BASE_DIR / "dataset" / "images" / "auto"
LABEL_DIR = BASE_DIR / "dataset" / "labels" / "auto"
MODEL_PATH = BASE_DIR / "yolov8n.pt"

# Ensure folders exist
IMAGE_DIR.mkdir(parents=True, exist_ok=True)
LABEL_DIR.mkdir(parents=True, exist_ok=True)

# Load YOLO model
print("🔍 Loading YOLO model...")
model = YOLO(str(MODEL_PATH))
print("✅ Model loaded successfully.")

# Process all videos
for video_path in VIDEO_DIR.glob("*.*"):
    if not video_path.suffix.lower() in [".mp4", ".avi", ".mov"]:
        continue
    print(f"\n🎞 Processing video: {video_path.name}")
    cap = cv2.VideoCapture(str(video_path))

    frame_idx = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_idx += 1
        frame_name = f"{video_path.stem}_{frame_idx:04d}.jpg"
        frame_path = IMAGE_DIR / frame_name
        cv2.imwrite(str(frame_path), frame)

        # Run YOLO detection
        results = model(frame)
        detections = results[0].boxes.data.cpu().numpy()

        label_path = LABEL_DIR / f"{frame_path.stem}.txt"
        with open(label_path, "w") as f:
            for det in detections:
                x1, y1, x2, y2, conf, cls = det
                if conf < 0.4:
                    continue
                # YOLO normalized format
                h, w, _ = frame.shape
                x_center = ((x1 + x2) / 2) / w
                y_center = ((y1 + y2) / 2) / h
                bw = (x2 - x1) / w
                bh = (y2 - y1) / h
                # Classify vehicles as "accident" if confidence high
                label = 0 if conf < 0.7 else 1  # 0=normal, 1=accident
                f.write(f"{label} {x_center:.6f} {y_center:.6f} {bw:.6f} {bh:.6f}\n")

    cap.release()

print("\n✅ Auto-labeling complete.")
print(f"Images saved in: {IMAGE_DIR}")
print(f"Labels saved in: {LABEL_DIR}")
print("You can now verify and correct labels using LabelImg.")
