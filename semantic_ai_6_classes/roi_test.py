import cv2
import os

os.makedirs("output", exist_ok=True)


def save_roi(image, box, name, index):
    """
    Save cropped ROI from detection box.
    """

    x1, y1, x2, y2 = map(int, box.xyxy[0])

    roi = image[y1:y2, x1:x2]

    roi_path = f"output/{name}_{index}.jpg"

    cv2.imwrite(roi_path, roi)

    return roi_path, roi

