from ultralytics import YOLO
from priority import PRIORITY
from roi import save_roi

import cv2

MODEL_PATH = "models/best.pt"
IMAGE_PATH = "test.jpg"

# Load model
model = YOLO(MODEL_PATH)

# Read image
image = cv2.imread(IMAGE_PATH)

# Run detection
results = model(IMAGE_PATH, conf=0.25)

count = 0

for result in results:

    for box in result.boxes:

        cls_id = int(box.cls[0])
        conf = float(box.conf[0])

        name = model.names[cls_id]
        priority = PRIORITY[name]

        roi_path, roi = save_roi(
            image,
            box,
            name,
            count
        )

        print("=" * 50)
        print(f"Detected   : {name}")
        print(f"Confidence : {conf:.2f}")
        print(f"Priority   : {priority}")
        print(f"ROI Saved  : {roi_path}")

        count += 1
