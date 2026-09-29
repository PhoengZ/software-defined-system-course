#!/usr/bin/env python3
"""
Benchmark Runner: Automates execution of storage benchmark matrix across EBS, Ephemeral NVMe, and S3.
Single-Run Execution Policy (Cost-optimized: 1 trial per configuration, no 3-trial averaging).
Saves output into benchmark_results.json.
"""

import os
import sys
import json
import glob
import shutil
import argparse
from test_fs import run_fs_benchmark
from test_s3 import run_s3_benchmark
import boto3

# Mapping of file sizes to actual files and iteration lists from 2110415 Storage Benchmark Template.xlsx
BENCHMARK_CONFIGS = [
    {
        "size_label": "2 KiB",
        "file_name": "2KiB-1105622-17903235018753.txt",
        "ebs_iterations": [32768, 65536, 131072, 262144, 393216],
        "eph_iterations": [32768, 65536, 131072, 262144, 393216],
        "s3_iterations": [512, 1024, 2048, 4096, 6144]
    },
    {
        "size_label": "256 KiB",
        "file_name": "256KiB-1105622-17903235361980.txt",
        "ebs_iterations": [512, 1024, 2048, 4096, 6144],
        "eph_iterations": [512, 1024, 2048, 4096, 6144],
        "s3_iterations": [512, 1024, 2048, 4096, 6144]
    },
    {
        "size_label": "1 MiB",
        "file_name": "1MiB-1105622-17903235676279.txt",
        "ebs_iterations": [128, 256, 512, 1024, 1536],
        "eph_iterations": [128, 256, 512, 1024, 1536],
        "s3_iterations": [128, 256, 512, 1024, 1536]
    },
    {
        "size_label": "128 MiB",
        "file_name": "random_large.172259.1571618485.0595.txt",
        "ebs_iterations": [1, 2, 4, 8, 12],
        "eph_iterations": [1, 2, 4, 8, 12],
        "s3_iterations": [1, 2, 4, 8, 12]
    }
]

def clean_fs_directory(target_dir: str):
    """Safely cleans up generated test files in the directory without deleting the directory itself."""
    if os.path.exists(target_dir):
        for entry in os.scandir(target_dir):
            try:
                if entry.is_file() or entry.is_symlink():
                    os.unlink(entry.path)
                elif entry.is_dir():
                    shutil.rmtree(entry.path)
            except Exception as e:
                print(f"Warning: Failed to delete {entry.path}: {e}", file=sys.stderr)

def clean_s3_bucket(bucket_name: str):
    """Deletes all objects in the S3 bucket to clean up after benchmark."""
    try:
        s3 = boto3.resource("s3")
        bucket = s3.Bucket(bucket_name)
        bucket.objects.all().delete()
    except Exception as e:
        print(f"Warning: Failed to clean S3 bucket {bucket_name}: {e}", file=sys.stderr)

def run_benchmarks(ebs_dir: str, eph_dir: str, bucket_name: str, skip_s3: bool = False, skip_fs: bool = False):
    results = {}

    for config in BENCHMARK_CONFIGS:
        label = config["size_label"]
        source_file = config["file_name"]
        results[label] = {
            "ebs": {},
            "ephemeral": {},
            "s3": {}
        }
        
        print(f"\n=======================================================")
        print(f"[*] Starting Benchmarks for: {label} (File: {source_file})")
        print(f"=======================================================")

        # 1. EBS Benchmark
        if not skip_fs and ebs_dir:
            print(f"\n--- Testing EBS ({ebs_dir}) ---")
            os.makedirs(ebs_dir, exist_ok=True)
            for n in config["ebs_iterations"]:
                clean_fs_directory(ebs_dir)
                print(f"-> EBS | {label} | N={n} ... ", end="", flush=True)
                total_time, per_file, bw = run_fs_benchmark(source_file, ebs_dir, n)
                results[label]["ebs"][n] = {
                    "total_write_time": total_time,
                    "write_time_per_file": per_file,
                    "bandwidth_mb_s": bw
                }
            clean_fs_directory(ebs_dir)

        # 2. Ephemeral Storage Benchmark
        if not skip_fs and eph_dir:
            print(f"\n--- Testing Ephemeral Storage ({eph_dir}) ---")
            os.makedirs(eph_dir, exist_ok=True)
            for n in config["eph_iterations"]:
                clean_fs_directory(eph_dir)
                print(f"-> Ephemeral | {label} | N={n} ... ", end="", flush=True)
                total_time, per_file, bw = run_fs_benchmark(source_file, eph_dir, n)
                results[label]["ephemeral"][n] = {
                    "total_write_time": total_time,
                    "write_time_per_file": per_file,
                    "bandwidth_mb_s": bw
                }
            clean_fs_directory(eph_dir)

        # 3. Amazon S3 Benchmark
        if not skip_s3 and bucket_name:
            print(f"\n--- Testing S3 (Bucket: {bucket_name}) ---")
            for n in config["s3_iterations"]:
                clean_s3_bucket(bucket_name)
                print(f"-> S3 | {label} | N={n} ... ", end="", flush=True)
                total_time, per_file, bw = run_s3_benchmark(source_file, bucket_name, n)
                results[label]["s3"][n] = {
                    "total_write_time": total_time,
                    "write_time_per_file": per_file,
                    "bandwidth_mb_s": bw
                }
            clean_s3_bucket(bucket_name)

    # Output to JSON
    output_json = "benchmark_results.json"
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"\n[+] All Benchmarks Completed! Results saved to '{output_json}'.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automate Activity 7 Storage Benchmarks (Single Run)")
    parser.add_argument("--ebs-dir", default=os.path.expanduser("~/ebs_test"), help="Directory path on EBS volume")
    parser.add_argument("--eph-dir", default="/mnt/eph", help="Directory path on Ephemeral NVMe mount")
    parser.add_argument("--bucket-name", default="", help="Name of the S3 test bucket")
    parser.add_argument("--skip-s3", action="store_true", help="Skip S3 benchmark")
    parser.add_argument("--skip-fs", action="store_true", help="Skip POSIX filesystem benchmarks")

    args = parser.parse_args()
    run_benchmarks(args.ebs_dir, args.eph_dir, args.bucket_name, args.skip_s3, args.skip_fs)
