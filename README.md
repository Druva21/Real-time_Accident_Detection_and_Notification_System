# Real-Time Accident Detection and Notification System

This project implements a real-time accident detection system using computer vision techniques.  
It processes video input to detect road accidents and can be extended to trigger alerts or notifications.

---

## Requirements

- Python 3.8 or higher
- VS Code
- Git
- pip

---

## Setup and Execution (VS Code)

### Step 1: Clone the repository

Open VS Code terminal and run:

git clone https://github.com/Druva21/Real-time_Accident_Detection_and_Notification_System.git  
cd Real-time_Accident_Detection_and_Notification_System

---

### Step 2: Create a virtual environment

python -m venv venv

Activate the virtual environment:

**Windows**
venv\Scripts\activate

**Linux / macOS**
source venv/bin/activate

---

### Step 3: Install dependencies

pip install -r requirements.txt

---

### Step 4: Prepare model weights

Ensure the required YOLO model weights file is available locally (for example: `yolov8n.pt`).  
This file should be placed in the project root directory.

---

### Step 5: Run the application

Run the main detection script:

python main.py

If training is required:

python train.py

---

## Output

- The system processes video input in real time.
- Accidents are detected and highlighted in the output.
- Results are displayed on the video feed.

---

## Screenshots and Results

Add screenshots after running the project:

![Accident Detection Output](images/output_1.png)
![Detection Visualization](images/output_2.png)

---

## Notes

- Large files such as datasets, videos, and trained models are excluded using `.gitignore`.
- Make sure the virtual environment is activated before running the scripts.

---

## Author

Druva Kumar Gorla  
Roll No: 2022BCD0018

---

## License

This project is intended for academic and educational purposes only.
