import os
import matplotlib.pyplot as plt

base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(base_dir, "result_credit")

def load_data(filepath):
    iterations = []
    times = []
    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(",")
            if len(parts) == 2:
                iterations.append(int(parts[0].strip()))
                times.append(float(parts[1].strip()))
    return iterations, times

host_file = os.path.join(data_dir, "result.txt")
cloud_credit_file = os.path.join(data_dir, "result1.txt")
cloud_no_credit_file = os.path.join(data_dir, "result2.txt")

iter_host, time_host = load_data(host_file)
iter_credit, time_credit = load_data(cloud_credit_file)
iter_nocredit, time_nocredit = load_data(cloud_no_credit_file)

plt.figure(figsize=(10, 6), dpi=300)

plt.plot(iter_nocredit, time_nocredit, label="1. Cloud t3.micro (No Credits)", color="#d62728", linewidth=1.5)
plt.plot(iter_credit, time_credit, label="2. Cloud t3.micro (With Credits)", color="#1f77b4", linewidth=1.5)
plt.plot(iter_host, time_host, label="3. Physical Machine (Host PC)", color="#2ca02c", linewidth=1.5)

plt.title("CPU Performance Comparison Across 3 Scenarios", fontsize=14, fontweight="bold", pad=12)
plt.xlabel("Iteration", fontsize=12)
plt.ylabel("Time (seconds) since 0'th round", fontsize=12)
plt.grid(True, linestyle="--", alpha=0.6)
plt.legend(fontsize=11, loc="upper left")

plt.tight_layout()
output_path = os.path.join(base_dir, "comparison_plot.png")
plt.savefig(output_path, dpi=300)
print(f"Graph saved successfully to: {output_path}")
