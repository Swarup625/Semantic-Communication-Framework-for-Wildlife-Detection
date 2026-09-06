import cv2
import numpy as np
import torch
import time

start = time.time()

from mobile_sam import sam_model_registry, SamPredictor

# -----------------------------------
# IMAGE
# -----------------------------------

IMAGE_PATH = "test.jpg"

# Replace with a YOLO box
BOX = np.array([404, 325, 838, 574])

# -----------------------------------
# LOAD SAM
# -----------------------------------

sam_checkpoint = "/home/admin/iit_project/MobileSAM/mobile_sam.pt"

model_type = "vit_t"

device = "cpu"

mobile_sam = sam_model_registry[model_type](
    checkpoint=sam_checkpoint
)

mobile_sam.to(device=device)

predictor = SamPredictor(mobile_sam)

# -----------------------------------
# LOAD IMAGE
# -----------------------------------

image = cv2.imread(IMAGE_PATH)

image_rgb = cv2.cvtColor(
    image,
    cv2.COLOR_BGR2RGB
)

predictor.set_image(image_rgb)

# -----------------------------------
# PREDICT MASK
# -----------------------------------

masks, scores, logits = predictor.predict(
    box=BOX,
    multimask_output=False
)

mask = masks[0]

# -----------------------------------
# SAVE MASK
# -----------------------------------

mask_img = (
    mask.astype(np.uint8) * 255
)

cv2.imwrite(
    "mask.png",
    mask_img
)

# -----------------------------------
# ANIMAL ONLY
# -----------------------------------

animal_only = np.zeros_like(image)

animal_only[mask] = image[mask]

cv2.imwrite(
    "animal_only.png",
    animal_only
)

end = time.time()

print(
    "SAM Time:",
    round(end-start, 2),
    "seconds"
)

print("Saved:")
print("mask.png")
print("animal_only.png")
