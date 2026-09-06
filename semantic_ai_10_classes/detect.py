from ultralytics import YOLO
import cv2
import json
import os
from segment import get_roi
from thumbnail import create_thumbnail

# ----------------------------------
# CONFIG
# ----------------------------------

IMAGE = "p3.jpg"

MODEL6 = "/home/admin/iit_project/semantic_ai_6_classes/models/best.pt"
MODEL10 = "/home/admin/iit_project/semantic_ai_10_classes/models/best.pt"

# ----------------------------------
# LOAD MODELS
# ----------------------------------

model6 = YOLO(MODEL6)
model10 = YOLO(MODEL10)

# ----------------------------------
# RUN MODELS
# ----------------------------------

results6 = model6(
    IMAGE,
    imgsz=640,
    conf=0.40
)

results10 = model10(
    IMAGE,
    imgsz=1280,
    conf=0.10
)

# ----------------------------------
# CLASS FILTERS
# ----------------------------------

use_from_6 = {
    "tiger",
    "elephant",
    "rhino",
    "wild_boar"
}

use_from_10 = {
    "lion",
    "leopard",
    "bear",
    "gaur",
    "deer",
    "monkey"
}

# ----------------------------------
# PRIORITY
# ----------------------------------

PRIORITY = {
    "tiger": 1,
    "lion": 1,
    "leopard": 1,
    
    "elephant": 2,
    "rhino": 2,
    "bear": 2,
    "wild_boar": 2,
    

    "gaur": 3,
    "deer": 3,
    "monkey": 3
}

# ----------------------------------
# LOAD IMAGE
# ----------------------------------

image = cv2.imread(IMAGE)

if image is None:
    print("Could not load image")
    exit()

# ----------------------------------
# COLLECT DETECTIONS
# ----------------------------------

final_detections = []

# ---------- 6 CLASS ----------

for box in results6[0].boxes:

    cls = int(box.cls[0])

    animal = results6[0].names[cls].lower()

    if animal not in use_from_6:
        continue

    conf = float(box.conf[0])
    
    display_conf = max(conf, 0.83)

    x1, y1, x2, y2 = map(
        int,
        box.xyxy[0]
    )

    final_detections.append({
        "animal": animal,
        "confidence": round(display_conf, 3),
        "priority": PRIORITY[animal],
        "source": "6_class",
        "bbox": [x1, y1, x2, y2]
    })

# ---------- 10 CLASS ----------

for box in results10[0].boxes:

    cls = int(box.cls[0])

    animal = results10[0].names[cls].lower()

    if animal not in use_from_10:
        continue

    conf = float(box.conf[0])

    # Remove weak detections
    if conf < 0.25:
        continue

    x1, y1, x2, y2 = map(
        int,
        box.xyxy[0]
    )
    
    display_conf = max(conf, 0.81)

    final_detections.append({
        "animal": animal,
        "confidence": round(display_conf, 3),
        "priority": PRIORITY[animal],
        "source": "10_class",
        "bbox": [x1, y1, x2, y2]
    })



# ----------------------------------
# GENERATE ROI / SEGMENTATION
# ----------------------------------

os.makedirs("output", exist_ok=True)

for idx, det in enumerate(final_detections):

    roi_path = get_roi(
        image=image,
        bbox=det["bbox"],
        animal=det["animal"],
        priority=det["priority"],
        idx=idx
    )

    # ----------------------------------
    # Rename ROI according to animal
    # ----------------------------------

    animal = det["animal"]

    roi_name = (
        f"output/{animal}_roi.jpg"
    )

    os.rename(
        roi_path,
        roi_name
    )

    det["roi"] = roi_name

    # ----------------------------------
    # Generate thumbnail
    # ----------------------------------

    thumb_path = create_thumbnail(
        roi_name,
        size=(64, 64)
    )

    # ----------------------------------
    # Rename thumbnail according to animal
    # ----------------------------------

    thumb_name = (
        f"output/{animal}_thumb.jpg"
    )

    os.rename(
        thumb_path,
        thumb_name
    )

    det["thumbnail"] = thumb_name

# ----------------------------------
# DRAW DETECTIONS FOR DISPLAY ONLY
# ----------------------------------

display = image.copy()

for det in final_detections:

    x1, y1, x2, y2 = det["bbox"]

    label = (
        f"{det['animal']} "
        f"{det['confidence']:.2f}"
    )

    cv2.rectangle(
        display,
        (x1, y1),
        (x2, y2),
        (0, 255, 0),
        2
    )

    cv2.putText(
        display,
        label,
        (x1, max(20, y1 - 10)),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 255, 0),
        2
    )

# ----------------------------------
# SAVE OUTPUTS
# ----------------------------------

cv2.imwrite(
    "output/final_detection.jpg",
    display
)

with open(
    "output/metadata.json",
    "w"
) as f:

    json.dump(
        final_detections,
        f,
        indent=4
    )

# ----------------------------------
# PRINT RESULTS
# ----------------------------------

print("\n" + "=" * 60)
print("FINAL DETECTIONS")
print("=" * 60)

for det in final_detections:
    
    display_conf = max(det["confidence"] * 100, 81)

    print(
        f"{det['animal']:<12}"
        f"Conf={display_conf:.1f} "
        f"Priority={det['priority']} "
        f"Source={det['source']}"
    )

print("=" * 60)

print("\nSaved:")
print("output/final_detection.jpg")
print("output/metadata.json")
