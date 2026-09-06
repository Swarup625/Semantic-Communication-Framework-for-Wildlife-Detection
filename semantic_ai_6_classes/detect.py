from ultralytics import YOLO
from priority import PRIORITY
from roi import save_roi
from metadata import create_metadata, save_metadata

import cv2

MODEL_PATH = "models/best.pt"
IMAGE_PATH = "test.jpg"

# Load model
model = YOLO(MODEL_PATH)

# Load image
image = cv2.imread(IMAGE_PATH)

# Run detection
results = model(IMAGE_PATH, conf=0.6)

all_detections = []

count = 0

for result in results:

    for box in result.boxes:

        cls_id = int(box.cls[0])
        conf = float(box.conf[0])

        name = model.names[cls_id]
        priority = PRIORITY[name]

        # Save ROI and thumbnail
        roi_path, thumb_path = save_roi(
            image,
            box,
            name,
            count
        )

        # Create metadata entry
        detection_metadata = create_metadata(
            animal=name,
            confidence=conf,
            priority=priority,
            thumb_path=thumb_path
        )

        all_detections.append(
            detection_metadata
        )

        print("=" * 50)
        print(f"Detected   : {name}")
        print(f"Confidence : {conf:.2f}")
        print(f"Priority   : {priority}")
        print(f"ROI Saved  : {roi_path}")
        print(f"Thumbnail  : {thumb_path}")

        count += 1

# Save all detections into one metadata file
save_metadata(all_detections)

print("\nMetadata saved to output/metadata.json")
print(f"Total detections: {len(all_detections)}")
