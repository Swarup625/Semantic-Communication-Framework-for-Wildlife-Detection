import cv2
import numpy as np

from mobile_sam import sam_model_registry
from mobile_sam import SamPredictor

# -----------------------------------
# LOAD SAM ONCE
# -----------------------------------

sam_checkpoint = "/home/admin/iit_project/MobileSAM/mobile_sam.pt"

model_type = "vit_t"

mobile_sam = sam_model_registry[model_type](
    checkpoint=sam_checkpoint
)

mobile_sam.to(device="cpu")

predictor = SamPredictor(mobile_sam)

# -----------------------------------
# SEGMENT FUNCTION
# -----------------------------------

def get_roi(
    image,
    bbox,
    animal,
    priority,
    idx
):

    x1, y1, x2, y2 = bbox

    # ---------------------------
    # LOW PRIORITY
    # ---------------------------

    if priority > 0:

        crop = image[y1:y2, x1:x2]

        path = (
            f"output/{animal}_{idx}_roi.jpg"
        )

        cv2.imwrite(path, crop)

        return path

    # ---------------------------
    # HIGH PRIORITY
    # ---------------------------

    image_rgb = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2RGB
    )

    predictor.set_image(image_rgb)

    box = np.array(
        [x1, y1, x2, y2]
    )

    masks, scores, logits = predictor.predict(
        box=box,
        multimask_output=False
    )

    mask = masks[0]

    segmented = np.zeros_like(image)

    segmented[mask] = image[mask]

    path = (
        f"output/{animal}_{idx}_segmented.png"
    )

    cv2.imwrite(path, segmented)

    return path
