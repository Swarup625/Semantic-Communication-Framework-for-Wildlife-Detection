import os
import random
import time
import psutil

# ----------------------------------
# CONFIG
# ----------------------------------

NUM_PACKETS = 100000

process = psutil.Process(os.getpid())

# ----------------------------------
# LOAD CHUNKS
# ----------------------------------

CHUNK_FOLDER = "./packets"

chunk_files = sorted(
    [
        f for f in os.listdir(CHUNK_FOLDER)
        if f.startswith("chunk_")
    ],
    key=lambda x: int(
        x.split("_")[1].split(".")[0]
    )
)

chunks = []

for chunk_name in chunk_files:

    with open(
        os.path.join(
            CHUNK_FOLDER,
            chunk_name
        ),
        "rb"
    ) as f:

        chunks.append(f.read())

TOTAL_CHUNKS = len(chunks)

if TOTAL_CHUNKS == 0:
    print("No chunks found")
    exit()

print(
    f"Loaded {TOTAL_CHUNKS} chunks"
)

# ----------------------------------
# BENCHMARK VARIABLES
# ----------------------------------

total_encode_time = 0

total_xor_bytes = 0

peak_ram = 0

cpu_time_start = process.cpu_times()

wall_start = time.perf_counter()

# ----------------------------------
# RATeless ENCODING TEST
# ----------------------------------

for packet_id in range(NUM_PACKETS):

    encode_start = time.perf_counter()

    r = random.random()

    if r < 0.8:
        degree = random.randint(1, 4)
    else:
        degree = random.randint(5, 10)

    degree = min(
        degree,
        TOTAL_CHUNKS
    )

    selected_indices = random.sample(
        range(TOTAL_CHUNKS),
        degree
    )

    encoded_data = bytearray(
        chunks[
            selected_indices[0]
        ]
    )

    for idx in selected_indices[1:]:

        chunk_data = chunks[idx]

        n = min(
            len(encoded_data),
            len(chunk_data)
        )

        total_xor_bytes += n

        for i in range(n):

            encoded_data[i] ^= (
                chunk_data[i]
            )

    encode_end = (
        time.perf_counter()
    )

    total_encode_time += (
        encode_end
        -
        encode_start
    )

    ram = (
        process.memory_info().rss
        /
        (1024 * 1024)
    )

    peak_ram = max(
        peak_ram,
        ram
    )

wall_end = time.perf_counter()

cpu_time_end = process.cpu_times()

# ----------------------------------
# RESULTS
# ----------------------------------

cpu_time_used = (

    cpu_time_end.user +
    cpu_time_end.system

) - (

    cpu_time_start.user +
    cpu_time_start.system

)

wall_time = (
    wall_end
    -
    wall_start
)

total_payload_bytes = sum(
    len(c)
    for c in chunks
)

encoding_throughput_mbps = (

    (
        total_payload_bytes
        *
        8
        *
        NUM_PACKETS
    )

    /

    total_encode_time

) / 1e6

cpu_efficiency = (

    total_xor_bytes

    /

    cpu_time_used

    if cpu_time_used > 0
    else 0

)

print()
print("=================================")
print("TX COMPUTATIONAL BENCHMARK")
print("=================================")

print(
    f"Packets Tested: "
    f"{NUM_PACKETS}"
)

print(
    f"Wall Time: "
    f"{wall_time:.4f} sec"
)

print(
    f"Pure Encoding Time: "
    f"{total_encode_time:.4f} sec"
)

print(
    f"Process CPU Time: "
    f"{cpu_time_used:.4f} sec"
)

print(
    f"Peak RAM: "
    f"{peak_ram:.2f} MB"
)

print(
    f"Total XOR Bytes: "
    f"{total_xor_bytes}"
)

print(
    f"Encoding Throughput: "
    f"{encoding_throughput_mbps:.3f} Mbps"
)

print(
    f"CPU Efficiency: "
    f"{cpu_efficiency:.2f} XOR-bytes/sec"
)

print("=================================")
