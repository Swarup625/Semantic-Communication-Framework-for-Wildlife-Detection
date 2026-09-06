import cv2
import os

# -----------------------------------
# CREATE THUMBNAIL
# -----------------------------------

def create_thumbnail(
    image_path,
    size=(64, 64)
):
    """
    Creates ultra-small thumbnail
    Target size: ~0.75–1 KB
    """

    image = cv2.imread(image_path)

    if image is None:
        print(f"Could not open {image_path}")
        return None

    thumb = cv2.resize(
        image,
        size,
        interpolation=cv2.INTER_AREA
    )

    filename = os.path.basename(image_path)

    name, ext = os.path.splitext(filename)

    thumb_path = f"output/thumb_{name}.jpg"

    cv2.imwrite(
        thumb_path,
        thumb,
        [
            cv2.IMWRITE_JPEG_QUALITY,
            30
        ]
    )

    size_kb = os.path.getsize(thumb_path) / 1024

    print(
        f"Thumbnail: {thumb_path} "
        f"({size_kb:.2f} KB)"
    )

    return thumb_path
