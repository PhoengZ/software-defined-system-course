#!/usr/bin/env python3
"""
Storage Benchmark: Amazon S3 (Object Storage)
Usage: python3 test_s3.py <source_file> <bucket_name> <n>
"""

import sys
import os
import time
import boto3

def run_s3_benchmark(source_file: str, bucket_name: str, n: int):
    if not os.path.exists(source_file):
        print(f"Error: Source file '{source_file}' does not exist.", file=sys.stderr)
        sys.exit(1)

    base_name = os.path.basename(source_file)
    file_size_bytes = os.path.getsize(source_file)

    # 1. Read input file into memory once
    with open(source_file, "rb") as f:
        data = f.read()

    # Pre-generate S3 object keys
    object_keys = [f"{base_name}_{i}" for i in range(n)]

    # Initialize S3 client using IAM Instance Profile or environment credentials
    s3_client = boto3.client("s3")

    # 2. Timing the upload of n objects
    t0 = time.time()
    for key in object_keys:
        s3_client.put_object(
            Bucket=bucket_name,
            Key=key,
            Body=data
        )
    t1 = time.time()

    total_time = t1 - t0
    total_bytes = file_size_bytes * n
    throughput_mb_s = (total_bytes / (total_time * 1_000_000)) if total_time > 0 else 0.0
    write_time_per_file = (total_time / n) if n > 0 else 0.0

    # Print results strictly at the end
    print(f"Total write time (s): {total_time:.4f}")
    print(f"Write time per file (s): {write_time_per_file:.6f}")
    print(f"Bandwidth (MB/s): {throughput_mb_s:.4f}")
    return total_time, write_time_per_file, throughput_mb_s

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 test_s3.py <source_file> <bucket_name> <n>", file=sys.stderr)
        sys.exit(1)

    source_path = sys.argv[1]
    s3_bucket = sys.argv[2]
    repetitions = int(sys.argv[3])

    run_s3_benchmark(source_path, s3_bucket, repetitions)
