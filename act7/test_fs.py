#!/usr/bin/env python3
"""
Storage Benchmark: POSIX Filesystem (EBS and Ephemeral Storage)
Usage: python3 test_fs.py <source_file> <target_dir> <n>
"""

import sys
import os
import time

def run_fs_benchmark(source_file: str, target_dir: str, n: int):
    if not os.path.exists(source_file):
        print(f"Error: Source file '{source_file}' does not exist.", file=sys.stderr)
        sys.exit(1)
        
    os.makedirs(target_dir, exist_ok=True)
    base_name = os.path.basename(source_file)
    file_size_bytes = os.path.getsize(source_file)
    
    # 1. Read input file into memory once
    with open(source_file, "rb") as f:
        data = f.read()

    # Pre-generate file paths to avoid string concatenation inside the timing loop
    target_paths = [os.path.join(target_dir, f"{base_name}_{i}") for i in range(n)]

    # 2. Timing the creation, write, and close of n files
    t0 = time.time()
    for path in target_paths:
        with open(path, "wb") as out_f:
            out_f.write(data)
    t1 = time.time()

    total_time = t1 - t0
    total_bytes = file_size_bytes * n
    # MB/s (Standard decimal MB = 1,000,000 Bytes, or MiB/s = 1,048,576 Bytes)
    throughput_mb_s = (total_bytes / (total_time * 1_000_000)) if total_time > 0 else 0.0
    write_time_per_file = (total_time / n) if n > 0 else 0.0

    # Print results strictly at the end
    print(f"Total write time (s): {total_time:.4f}")
    print(f"Write time per file (s): {write_time_per_file:.6f}")
    print(f"Bandwidth (MB/s): {throughput_mb_s:.4f}")
    return total_time, write_time_per_file, throughput_mb_s

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 test_fs.py <source_file> <target_dir> <n>", file=sys.stderr)
        sys.exit(1)

    source_path = sys.argv[1]
    target_directory = sys.argv[2]
    repetitions = int(sys.argv[3])

    run_fs_benchmark(source_path, target_directory, repetitions)
