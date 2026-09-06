import json
import time


def create_metadata(
    animal,
    confidence,
    priority,
    thumb_path
):

    return {
        "animal": animal,
        "confidence": round(confidence, 3),
        "priority": priority,
        "thumbnail": thumb_path
    }


def save_metadata(all_detections):

    metadata = {
        "timestamp": int(time.time()),
        "num_detections": len(all_detections),
        "detections": all_detections
    }

    with open(
        "output/metadata.json",
        "a"
    ) as f:

        json.dump(
            metadata,
            f,
            indent=4
        )
