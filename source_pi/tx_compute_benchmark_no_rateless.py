import os
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

total_processing_time = 0

peak_ram = 0

cpu_time_start = process.cpu_times()

wall_start = time.perf_counter()

total_bytes_processed = 0

# ----------------------------------
# DIRECT TRANSMISSION TEST
# ----------------------------------

for packet_id in range(NUM_PACKETS):

    start = time.perf_counter()

    # Select one chunk exactly as-is
    chunk = chunks[
        packet_id % TOTAL_CHUNKS
    ]

    # Simulate packet preparation
    payload = bytes(chunk)

    total_bytes_processed += len(payload)

    end = time.perf_counter()

    total_processing_time += (
        end - start
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

throughput_mbps = (

    (
        total_bytes_processed
        * 8
    )

    /

    total_processing_time

) / 1e6 if total_processing_time > 0 else 0

packets_per_sec = (

    NUM_PACKETS
    /
    total_processing_time

) if total_processing_time > 0 else 0

print()
print("=================================")
print("TX BENCHMARK (NO RATELESS)")
print("=================================")

print(
    f"Packets Tested: "
    f"{NUM_PACKETS}"
)

print(
    f"Wall Time: "
    f"{wall_time:.6f} sec"
)

print(
    f"Processing Time: "
    f"{total_processing_time:.6f} sec"
)

print(
    f"Process CPU Time: "
    f"{cpu_time_used:.6f} sec"
)

print(
    f"Peak RAM: "
    f"{peak_ram:.2f} MB"
)

print(
    f"Total Bytes Processed: "
    f"{total_bytes_processed}"
)

print(
    f"Throughput: "
    f"{throughput_mbps:.3f} Mbps"
)

print(
    f"Packets/sec: "
    f"{packets_per_sec:.2f}"
)

print("=================================")
