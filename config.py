CONFIG = {
    "yolo_model": "models/best.pt",  # trained model will be placed here after training; fallback to 'yolov8n.pt' if missing
    "confidence_threshold": 0.4,
    "vehicle_classes": [2, 3, 5, 7],
    "emergency_severity_threshold": 0.6,
    "alert_cooldown": 30,
    "frame_extract_fps": 2
}
