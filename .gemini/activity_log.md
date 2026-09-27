# Activity Log

- **Attempt**: Create `.gitignore` to ignore `lectures/` directory.
- **Hypothesis**: Writing `lectures/` into `.gitignore` at the project root will cause Git to stop tracking the `lectures` directory.
- **Outcome**: Successfully created the file.

## 2026-09-27: Generate log_plot.png in plot_comparison.py
- **Attempt**: Updated `act6/plot_comparison.py` to create and save a logarithmic scale graph `log_plot.png` alongside `comparison_plot.png`.
- **Hypothesis**: Adding a second figure with `plt.yscale("log")` will generate `log_plot.png` displaying iteration vs time on a log scale without affecting `comparison_plot.png`.
- **Outcome**: Script executed successfully (exit code 0). Both `comparison_plot.png` and `log_plot.png` were created cleanly.

## 2026-09-27: Update act6/sol.md with new images and updated benchmark analysis
- **Attempt**: Updated `act6/sol.md` by replacing outdated screenshots with `cpu_credit.png` and `cpu_nocredit.png`, adding `log_plot.png` alongside `comparison_plot.png`, updating the timing comparison table with latest benchmark measurements (Scenario 1: 0.15418858s, Scenario 2: 0.00991503s, Host PC: 0.01318360s), and updating answers to Part 4 questions 2, 3, and 4.
- **Hypothesis**: Updating `sol.md` with accurate timing measurements, clear dual-scale plots, and CloudWatch metrics provides an accurate and thorough report matching the real system behavior.
- **Outcome**: `act6/sol.md` updated successfully with consistent data and structure.
