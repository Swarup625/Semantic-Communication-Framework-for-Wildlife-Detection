import cv2
import os

os.makedirs("output", exist_ok=True)

def save_roi(image, box, name, index):

    x1, y1, x2, y2 = map(int, box.xyxy[0])

    roi = image[y1:y2, x1:x2]

    roi_path = f"output/{name}_{index}.jpg"

    cv2.imwrite(roi_path, roi)

    # Thumbnail
    thumb = cv2.resize(roi, (64, 64))

    thumb_path = f"output/thumb_{name}_{index}.jpg"

    cv2.imwrite(
        thumb_path,
        thumb,
        [cv2.IMWRITE_JPEG_QUALITY, 30]
    )

    return roi_path, thumb_path
