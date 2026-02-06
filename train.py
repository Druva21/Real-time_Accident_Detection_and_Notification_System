import os
from ultralytics import YOLO

# === PATH SETUP ===
BASE = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE, 'dataset')
AUTO_IMAGES = os.path.join(DATA_DIR, 'images', 'auto')
AUTO_LABELS = os.path.join(DATA_DIR, 'labels', 'auto')
MODELS_DIR = os.path.join(BASE, 'models')
os.makedirs(MODELS_DIR, exist_ok=True)

print("✅ Using Auto-labeled Dataset for Training")
print("Images Path:", AUTO_IMAGES)
print("Labels Path:", AUTO_LABELS)

# === CREATE DATA.YAML FOR YOLO TRAINING ===
yaml_path = os.path.join(DATA_DIR, 'auto_data.yaml')
with open(yaml_path, 'w') as f:
    f.write(f"""
train: {AUTO_IMAGES}
val: {AUTO_IMAGES}

nc: 2
names: ['Normal', 'Accident']
""")

print("📁 YOLO Dataset YAML created at:", yaml_path)

# === LOAD YOLO MODEL AND TRAIN ===
print("🚀 Starting YOLOv8 Training on Auto-labeled Dataset...")
model = YOLO('yolov8n.pt')  # You can change to yolov8s.pt for better accuracy

results = model.train(
    data=yaml_path,
    epochs=5,             
    imgsz=640,
    batch=8,
    project=MODELS_DIR,
    name='auto_trained_model'
)

print("\n✅ Training complete!")
print("📍 Model saved at:", os.path.join(MODELS_DIR, 'auto_trained_model'))
