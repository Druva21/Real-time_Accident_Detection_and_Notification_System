ACCIDENT DETECTION - Final Project Package

Included files:
- config.py : configuration (model path, thresholds)
- alert_manager.py : handles GUI/console alerts with cooldown
- motion_detector.py : optical flow function
- video_manager.py : camera/video capture helper
- train.py : extract frames & (optionally) train script
- main.py : Tkinter GUI app (Start Camera / Upload Video / Start Processing)
- accident_videos/ : copied from your uploaded zip (if present)
- models/ : place to store trained models (best.pt will be copied here after training)
- requirements.txt : pip install -r requirements.txt

Quick start:
1) Install dependencies:
   pip install -r requirements.txt
2) Place your videos in accident_videos/ (already copied if provided)
3) Extract frames and prepare dataset & labels:
   python train.py
   - This extracts frames into dataset/images and creates dataset.yaml
   - You MUST annotate dataset/images/train and dataset/images/val using LabelImg or similar
4) After annotation, re-run python train.py to start training (it will detect labels and call ultralytics training)
5) After training completes, best.pt will be copied to models/best.pt
6) Run GUI:
   python main.py

Notes:
- Training requires labeled data. The script helps extract frames; labeling must be manual/assisted.
- Thresholds can be tuned in config.py
