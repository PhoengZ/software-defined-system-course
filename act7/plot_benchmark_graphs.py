#!/usr/bin/env python3
"""
Plot Benchmark Charts for Activity 7 Report:
Graph 1: File Size vs Throughput (MB/s)
Graph 2: Number of Files (Iterations) vs Throughput / Performance
"""

import json
import matplotlib.pyplot as plt
import numpy as np

def generate_plots():
    with open("benchmark_results.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # Style configuration
    plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
    plt.rcParams.update({"font.size": 11, "figure.autolayout": True})

    # =========================================================================
    # GRAPH 1: File Size vs Throughput (MB/s)
    # Using the highest iteration of each file size to represent peak sustained bandwidth
    # =========================================================================
    file_sizes = ["2 KiB", "256 KiB", "1 MiB", "128 MiB"]
    
    ebs_throughputs = []
    eph_throughputs = []
    s3_throughputs = []

    for size in file_sizes:
        # Get the max iteration for each storage
        ebs_max_n = str(max([int(k) for k in data[size]["ebs"].keys()]))
        eph_max_n = str(max([int(k) for k in data[size]["ephemeral"].keys()]))
        s3_max_n = str(max([int(k) for k in data[size]["s3"].keys()]))

        ebs_throughputs.append(data[size]["ebs"][ebs_max_n]["bandwidth_mb_s"])
        eph_throughputs.append(data[size]["ephemeral"][eph_max_n]["bandwidth_mb_s"])
        s3_throughputs.append(data[size]["s3"][s3_max_n]["bandwidth_mb_s"])

    x = np.arange(len(file_sizes))
    width = 0.25

    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    rects1 = ax.bar(x - width, ebs_throughputs, width, label="AWS EBS (gp3)", color="#2b5c8f")
    rects2 = ax.bar(x, eph_throughputs, width, label="Ephemeral Storage (NVMe)", color="#e07a5f")
    rects3 = ax.bar(x + width, s3_throughputs, width, label="Amazon S3 (Boto3)", color="#81b29a")

    ax.set_ylabel("Throughput / Bandwidth (MB/s)", fontweight="bold")
    ax.set_xlabel("File Size", fontweight="bold")
    ax.set_title("Graph 1: Storage Throughput vs. File Size (Activity 7)", fontsize=14, fontweight="bold", pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(file_sizes, fontweight="bold")
    ax.legend(frameon=True)

    # Label values on bars
    for rects in [rects1, rects2, rects3]:
        for rect in rects:
            height = rect.get_height()
            if height > 0:
                ax.annotate(f"{height:.1f}",
                            xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0, 3),  # 3 points vertical offset
                            textcoords="offset points",
                            ha="center", va="bottom", fontsize=8, rotation=0)

    plt.savefig("graph1_file_size_vs_throughput.png")
    plt.close()
    print("[+] Graph 1 saved as 'graph1_file_size_vs_throughput.png'")

    # =========================================================================
    # GRAPH 2: Iterations vs Throughput (Linearity Check across File Sizes)
    # =========================================================================
    fig, axes = plt.subplots(2, 2, figsize=(14, 10), dpi=300)
    fig.suptitle("Graph 2: Number of Files (Iterations) vs. Performance (Linearity Test)", fontsize=16, fontweight="bold")

    plot_configs = [
        ("2 KiB", axes[0, 0]),
        ("256 KiB", axes[0, 1]),
        ("1 MiB", axes[1, 0]),
        ("128 MiB", axes[1, 1])
    ]

    for label, ax in plot_configs:
        ebs_items = sorted([(int(k), v["bandwidth_mb_s"]) for k, v in data[label]["ebs"].items()])
        eph_items = sorted([(int(k), v["bandwidth_mb_s"]) for k, v in data[label]["ephemeral"].items()])
        s3_items = sorted([(int(k), v["bandwidth_mb_s"]) for k, v in data[label]["s3"].items()])

        ax.plot([x[0] for x in ebs_items], [x[1] for x in ebs_items], marker="o", linewidth=2, label="EBS", color="#2b5c8f")
        ax.plot([x[0] for x in eph_items], [x[1] for x in eph_items], marker="s", linewidth=2, label="Ephemeral", color="#e07a5f")
        ax.plot([x[0] for x in s3_items], [x[1] for x in s3_items], marker="^", linewidth=2, label="S3", color="#81b29a")

        ax.set_title(f"File Size: {label}", fontweight="bold")
        ax.set_xlabel("Number of Files (N)", fontsize=10)
        ax.set_ylabel("Bandwidth (MB/s)", fontsize=10)
        ax.legend(frameon=True)

    plt.tight_layout()
    plt.savefig("graph2_iterations_vs_performance.png")
    plt.close()
    print("[+] Graph 2 saved as 'graph2_iterations_vs_performance.png'")

if __name__ == "__main__":
    generate_plots()
