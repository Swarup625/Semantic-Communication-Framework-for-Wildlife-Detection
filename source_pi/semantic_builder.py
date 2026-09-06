import os
import json
import zipfile

OUTPUT_DIR = (
    "/home/admin/iit_project/"
    "semantic_ai_10_classes/output"
)

EVENT_ZIP = (
    f"{OUTPUT_DIR}/event.zip"
)


def build_event():

    metadata_file = (
        f"{OUTPUT_DIR}/metadata.json"
    )

    if not os.path.exists(metadata_file):

        raise FileNotFoundError(
            "metadata.json not found"
        )

    with open(metadata_file, "r") as f:

        detections = json.load(f)

    if os.path.exists(EVENT_ZIP):

        os.remove(EVENT_ZIP)

    with zipfile.ZipFile(
        EVENT_ZIP,
        "w",
        zipfile.ZIP_DEFLATED
    ) as z:

        # Always include metadata
        z.write(
            metadata_file,
            "metadata.json"
        )

        # Process every detection
        for idx, det in enumerate(detections):

            animal = det["animal"]
            priority = det["priority"]

            # --------------------
            # Priority 1
            # ROI + JSON
            # --------------------

            if priority == 1:

                roi_file = (
                    f"{OUTPUT_DIR}/"
                    f"{animal}_roi.jpg"
                )

                if os.path.exists(roi_file):

                    z.write(
                        roi_file,
                        os.path.basename(
                            roi_file
                        )
                    )

                    print(
                        f"Added ROI: "
                        f"{os.path.basename(roi_file)}"
                    )

            # --------------------
            # Priority 2
            # Thumbnail + JSON
            # --------------------

            elif priority == 2:

                thumb_file = (
                    f"{OUTPUT_DIR}/"
                    f"{animal}_thumb.jpg"
                )

                if os.path.exists(thumb_file):

                    z.write(
                        thumb_file,
                        os.path.basename(
                            thumb_file
                        )
                    )

                    print(
                        f"Added Thumbnail: "
                        f"{os.path.basename(thumb_file)}"
                    )

            # --------------------
            # Priority 3
            # JSON only
            # --------------------

            else:

                print(
                    f"JSON only: "
                    f"{animal}"
                )

    print(
        f"\nCreated: {EVENT_ZIP}"
    )

    return EVENT_ZIP
