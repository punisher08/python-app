

import cv2
from ultralytics import YOLO

# Get color based on label
def get_color_by_label(label):
    color_map = {
        'person': (0, 255, 0),        # Green
        'cell phone': (255, 0, 0),    # Blue
        'camera': (0, 0, 255),        # Red
        'tv': (255, 255, 0),          # Cyan
        'laptop': (255, 0, 255),      # Magenta
    }
    return color_map.get(label, (255, 255, 255))  # Default to white if not mapped

# Load YOLOv8 model
model = YOLO("yolov8l.pt")  

# Scan for available cameras (indexes 0–5)
def list_available_cameras(max_index=5):
    print("🔍 Scanning for available cameras...")
    available = []
    for i in range(max_index):
        cap = cv2.VideoCapture(i)
        if cap.read()[0]:
            print(f"✅ Camera found at index {i}")
            available.append(i)
            cap.release()
    if not available:
        print("❌ No cameras found.")
    return available

# List and select camera
available_cams = list_available_cameras()
if not available_cams:
    exit()

selected = int(input(f"\n🎥 Enter camera index to use from {available_cams}: "))
cap = cv2.VideoCapture(selected)

if not cap.isOpened():
    print("❌ Failed to open selected camera.")
    exit()

print("📷 Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Failed to read frame.")
        break

    results = model(frame)

    for result in results:
        for box in result.boxes:
            cls_id = int(box.cls[0])
            confidence = float(box.conf[0])
            label = model.names[cls_id]
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            print(label)

            if label in ['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', ...]:

                color = get_color_by_label(label)
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, f"{label} {confidence:.2f}", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    cv2.imshow("Camera Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

