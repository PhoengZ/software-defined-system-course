#!/usr/bin/env python3
"""
Plot Benchmark Charts for Activity 7 Report Matching Professor's Specification:
Graph 1: Total Bytes Written vs. Throughput (Normalized by Total Bytes Written as per PDF hint)
- EBS: 2KiB, 256KiB, 1MiB, 128MiB across Total Bytes Written (128MiB, 256MiB, 512MiB, 1GiB, 1.5GiB)
- Ephemeral: 2KiB, 256KiB, 1MiB, 128MiB
- S3: 2KiB, 256KiB, 1MiB, 128MiB
- Overall comparison across storage systems
Graph 2: Number of Files (Iterations) vs. Performance (Total Time & Throughput Linearity)
"""

import json
import matplotlib.pyplot as plt
import numpy as np

def run_plotting():
    with open("benchmark_results.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
    plt.rcParams.update({"font.size": 11, "figure.autolayout": True})

    # Normalized standard Total Bytes Written points (128 MiB to 1.5 GiB)
    common_x_labels = ["128 MiB", "256 MiB", "512 MiB", "1 GiB", "1.5 GiB"]

    # Mapping sizes to total bytes in MiB
    # 256 KiB (0.25 MiB): [512->128, 1024->256, 2048->512, 4096->1024, 6144->1536]
    # 1 MiB (1 MiB): [128->128, 256->256, 512->512, 1024->1024, 1536->1536]
    # 128 MiB (128 MiB): [1->128, 2->256, 4->512, 8->1024, 12->1536]
    # 2 KiB EBS/Eph: [32768->64, 65536->128, 131072->256, 262144->512, 393216->768]

    # =========================================================================
    # GRAPH 1A: EBS - Total Bytes Written vs Throughput (Exact Match to Professor's Example)
    # =========================================================================
    plt.figure(figsize=(10, 6), dpi=300)
    
    # 128 MiB line
    ebs_128mib = [data["128 MiB"]["ebs"][str(n)]["bandwidth_mb_s"] for n in [1, 2, 4, 8, 12]]
    # 1 MiB line
    ebs_1mib = [data["1 MiB"]["ebs"][str(n)]["bandwidth_mb_s"] for n in [128, 256, 512, 1024, 1536]]
    # 256 KiB line
    ebs_256kib = [data["256 KiB"]["ebs"][str(n)]["bandwidth_mb_s"] for n in [512, 1024, 2048, 4096, 6144]]
    # 2 KiB line (all 5 test points matching professor's 5-row spreadsheet template)
    ebs_2kib = [data["2 KiB"]["ebs"][str(n)]["bandwidth_mb_s"] for n in [32768, 65536, 131072, 262144, 393216]]

    plt.plot(common_x_labels, ebs_256kib, marker="o", linewidth=2.5, label="EBS 256KiB", color="#e74c3c")
    plt.plot(common_x_labels, ebs_1mib, marker="s", linewidth=2.5, label="EBS 1MiB", color="#f39c12")
    plt.plot(common_x_labels, ebs_128mib, marker="^", linewidth=2.5, label="EBS 128MiB", color="#27ae60")
    plt.plot(common_x_labels, ebs_2kib, marker="D", linewidth=2.5, label="EBS 2KiB", color="#2980b9")

    plt.title("Total Bytes Written vs Throughput (AWS EBS)", fontsize=14, fontweight="bold", pad=15)
    plt.xlabel("Total Bytes Written", fontweight="bold")
    plt.ylabel("Throughput (MB/s)", fontweight="bold")
    plt.legend(frameon=True, loc="upper right")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.savefig("graph1_ebs_total_bytes_vs_throughput.png")
    plt.close()
    print("[+] Saved 'graph1_ebs_total_bytes_vs_throughput.png'")

    # =========================================================================
    # GRAPH 1B: Ephemeral - Total Bytes Written vs Throughput
    # =========================================================================
    plt.figure(figsize=(10, 6), dpi=300)
    eph_128mib = [data["128 MiB"]["ephemeral"][str(n)]["bandwidth_mb_s"] for n in [1, 2, 4, 8, 12]]
    eph_1mib = [data["1 MiB"]["ephemeral"][str(n)]["bandwidth_mb_s"] for n in [128, 256, 512, 1024, 1536]]
    eph_256kib = [data["256 KiB"]["ephemeral"][str(n)]["bandwidth_mb_s"] for n in [512, 1024, 2048, 4096, 6144]]
    eph_2kib = [data["2 KiB"]["ephemeral"][str(n)]["bandwidth_mb_s"] for n in [32768, 65536, 131072, 262144, 393216]]

    plt.plot(common_x_labels, eph_256kib, marker="o", linewidth=2.5, label="Ephemeral 256KiB", color="#e74c3c")
    plt.plot(common_x_labels, eph_1mib, marker="s", linewidth=2.5, label="Ephemeral 1MiB", color="#f39c12")
    plt.plot(common_x_labels, eph_128mib, marker="^", linewidth=2.5, label="Ephemeral 128MiB", color="#27ae60")
    plt.plot(common_x_labels, eph_2kib, marker="D", linewidth=2.5, label="Ephemeral 2KiB", color="#2980b9")

    plt.title("Total Bytes Written vs Throughput (Ephemeral Storage NVMe)", fontsize=14, fontweight="bold", pad=15)
    plt.xlabel("Total Bytes Written", fontweight="bold")
    plt.ylabel("Throughput (MB/s)", fontweight="bold")
    plt.legend(frameon=True, loc="upper right")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.savefig("graph1_ephemeral_total_bytes_vs_throughput.png")
    plt.close()
    print("[+] Saved 'graph1_ephemeral_total_bytes_vs_throughput.png'")

    # =========================================================================
    # GRAPH 1C: Amazon S3 - Total Bytes Written vs Throughput
    # =========================================================================
    plt.figure(figsize=(10, 6), dpi=300)
    s3_128mib = [data["128 MiB"]["s3"][str(n)]["bandwidth_mb_s"] for n in [1, 2, 4, 8, 12]]
    s3_1mib = [data["1 MiB"]["s3"][str(n)]["bandwidth_mb_s"] for n in [128, 256, 512, 1024, 1536]]
    s3_256kib = [data["256 KiB"]["s3"][str(n)]["bandwidth_mb_s"] for n in [512, 1024, 2048, 4096, 6144]]
    s3_2kib = [data["2 KiB"]["s3"][str(n)]["bandwidth_mb_s"] for n in [512, 1024, 2048, 4096, 6144]]

    plt.plot(common_x_labels, s3_256kib, marker="o", linewidth=2.5, label="S3 256KiB", color="#e74c3c")
    plt.plot(common_x_labels, s3_1mib, marker="s", linewidth=2.5, label="S3 1MiB", color="#f39c12")
    plt.plot(common_x_labels, s3_128mib, marker="^", linewidth=2.5, label="S3 128MiB", color="#27ae60")
    plt.plot(common_x_labels, s3_2kib, marker="D", linewidth=2.5, label="S3 2KiB (~0.07 MB/s)", color="#2980b9")

    # Add text annotation for S3 2KiB so its precise value is readable despite large scale
    plt.annotate(
        f"S3 2KiB: {s3_2kib[1]:.2f} MB/s",
        xy=(1, s3_2kib[1]),
        xytext=(1, 4.0),
        arrowprops=dict(facecolor="#2980b9", shrink=0.15, width=1.5, headwidth=6),
        ha="center",
        fontweight="bold",
        color="#2980b9",
        fontsize=10
    )

    plt.title("Total Bytes Written vs Throughput (Amazon S3)", fontsize=14, fontweight="bold", pad=15)
    plt.xlabel("Total Bytes Written", fontweight="bold")
    plt.ylabel("Throughput (MB/s)", fontweight="bold")
    plt.legend(frameon=True, loc="upper left")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.savefig("graph1_s3_total_bytes_vs_throughput.png")
    plt.close()
    print("[+] Saved 'graph1_s3_total_bytes_vs_throughput.png'")

    # =========================================================================
    # GRAPH 1D: Combined 3-in-1 Comparison across all 4 File Sizes
    # =========================================================================
    plt.figure(figsize=(11, 6), dpi=300)
    sizes = ["2 KiB", "256 KiB", "1 MiB", "128 MiB"]
    ebs_comp = [
        data["2 KiB"]["ebs"]["393216"]["bandwidth_mb_s"],
        data["256 KiB"]["ebs"]["4096"]["bandwidth_mb_s"],
        data["1 MiB"]["ebs"]["1024"]["bandwidth_mb_s"],
        data["128 MiB"]["ebs"]["8"]["bandwidth_mb_s"]
    ]
    eph_comp = [
        data["2 KiB"]["ephemeral"]["393216"]["bandwidth_mb_s"],
        data["256 KiB"]["ephemeral"]["4096"]["bandwidth_mb_s"],
        data["1 MiB"]["ephemeral"]["1024"]["bandwidth_mb_s"],
        data["128 MiB"]["ephemeral"]["8"]["bandwidth_mb_s"]
    ]
    s3_comp = [
        data["2 KiB"]["s3"]["6144"]["bandwidth_mb_s"],
        data["256 KiB"]["s3"]["4096"]["bandwidth_mb_s"],
        data["1 MiB"]["s3"]["1024"]["bandwidth_mb_s"],
        data["128 MiB"]["s3"]["8"]["bandwidth_mb_s"]
    ]

    x = np.arange(len(sizes))
    w = 0.25
    plt.bar(x - w, ebs_comp, width=w, label="EBS", color="#2b5c8f")
    plt.bar(x, eph_comp, width=w, label="Ephemeral", color="#e07a5f")
    plt.bar(x + w, s3_comp, width=w, label="S3", color="#81b29a")

    for i in range(len(sizes)):
        plt.text(i - w, ebs_comp[i] + 3, f"{ebs_comp[i]:.1f}", ha="center", fontsize=9, fontweight="bold")
        plt.text(i, eph_comp[i] + 3, f"{eph_comp[i]:.1f}", ha="center", fontsize=9, fontweight="bold")
        plt.text(i + w, s3_comp[i] + 3, f"{s3_comp[i]:.2f}", ha="center", fontsize=9, fontweight="bold")

    plt.xticks(x, sizes, fontweight="bold")
    plt.xlabel("File Size (2KiB, 256KiB, 1MiB, 128MiB)", fontweight="bold")
    plt.ylabel("Throughput (MB/s)", fontweight="bold")
    plt.title("Graph 1: Normalized Storage Throughput vs. File Size (All Storage Types)", fontsize=14, fontweight="bold", pad=15)
    plt.legend(frameon=True)
    plt.grid(True, linestyle="--", alpha=0.5, axis="y")
    plt.savefig("graph1_file_size_vs_throughput.png")
    plt.close()
    print("[+] Saved 'graph1_file_size_vs_throughput.png'")

    # =========================================================================
    # GRAPH 2: Iterations vs Total Write Time (Showing Linear Scaling T ~ N)
    # =========================================================================
    fig, axes = plt.subplots(2, 2, figsize=(14, 10), dpi=300)
    fig.suptitle("Graph 2: Number of Files (Iterations) vs. Total Write Time (Linearity Check)", fontsize=16, fontweight="bold")

    plot_configs = [
        ("2 KiB", axes[0, 0]),
        ("256 KiB", axes[0, 1]),
        ("1 MiB", axes[1, 0]),
        ("128 MiB", axes[1, 1])
    ]

    for label, ax in plot_configs:
        ebs_items = sorted([(int(k), v["total_write_time"]) for k, v in data[label]["ebs"].items()])
        eph_items = sorted([(int(k), v["total_write_time"]) for k, v in data[label]["ephemeral"].items()])
        s3_items = sorted([(int(k), v["total_write_time"]) for k, v in data[label]["s3"].items()])

        ax.plot([x[0] for x in ebs_items], [x[1] for x in ebs_items], marker="o", linewidth=2, label="EBS", color="#2b5c8f")
        ax.plot([x[0] for x in eph_items], [x[1] for x in eph_items], marker="s", linewidth=2, label="Ephemeral", color="#e07a5f")
        ax.plot([x[0] for x in s3_items], [x[1] for x in s3_items], marker="^", linewidth=2, label="S3", color="#81b29a")

        ax.set_title(f"File Size: {label}", fontweight="bold")
        ax.set_xlabel("Number of Files (N)", fontsize=10)
        ax.set_ylabel("Total Write Time (seconds)", fontsize=10)
        ax.legend(frameon=True)
        ax.grid(True, linestyle="--", alpha=0.6)

    plt.tight_layout()
    plt.savefig("graph2_iterations_vs_performance.png")
    plt.close()
    print("[+] Saved 'graph2_iterations_vs_performance.png'")

if __name__ == "__main__":
    run_plotting()
