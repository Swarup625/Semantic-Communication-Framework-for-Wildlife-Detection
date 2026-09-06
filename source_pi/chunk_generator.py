import os
import shutil

PACKET_DIR = (
    "/home/admin/iit_project/"
    "source_pi/packets"
)

CHUNK_SIZE = 128


def generate_chunks(input_file):

    if os.path.exists(PACKET_DIR):
        shutil.rmtree(PACKET_DIR)

    os.makedirs(
        PACKET_DIR,
        exist_ok=True
    )

    with open(
        input_file,
        "rb"
    ) as f:

        data = f.read()

    original_size = len(data)

    chunk_count = 0

    for i in range(
        0,
        original_size,
        CHUNK_SIZE
    ):

        chunk = data[i:i+CHUNK_SIZE]

        # -------------------------
        # PAD LAST CHUNK
        # -------------------------

        if len(chunk) < CHUNK_SIZE:

            padding = (
                CHUNK_SIZE
                -
                len(chunk)
            )

            chunk += bytes(padding)

        chunk_file = (
            f"{PACKET_DIR}/"
            f"chunk_{chunk_count}.bin"
        )

        with open(
            chunk_file,
            "wb"
        ) as c:

            c.write(chunk)

        chunk_count += 1

    print(
        f"Generated {chunk_count} chunks"
    )

    print(
        f"Original Size: "
        f"{original_size} bytes"
    )

    print(
        f"Chunk Size: "
        f"{CHUNK_SIZE} bytes"
    )

    return (
        chunk_count,
        original_size
    )
