# Activity Log

## [2026-09-15T21:00:30+07:00] - Part 3: Comparison Table Setup
- **Topic**: Setup Comparison Table in `sol.md` for CPU performance analysis.
- **What was attempted**: Created Markdown comparison table in `sol.md` matching Part 3 specifications of Activity 6 lab with existing measurement data from `result.txt` (Host PC) and `result1.txt` (EC2 with Credits).
- **Hypothesis being tested**: Structuring the table with measured metrics (seconds and microseconds) provides clear side-by-side comparison across the 3 scenarios.
- **Observed result/outcome**: Pending user's final data from Scenario 1 (No Credits) to complete the full dataset.

## [2026-09-15T21:23:00+07:00] - Part 3: Comparison Table Completion (No Credits Scenario)
- **Topic**: Record Scenario 1 (No Credits) results from `result_credit/result2.txt` into `sol.md`.
- **What was attempted**: Parsed `result_credit/result2.txt` (Total time: 0.00991012s / 9,910.12µs) and updated the comparison table in `sol.md`.
- **Hypothesis being tested**: Cloud instance with depleted credits will show higher total execution time compared to Cloud instance with credits due to CPU quota throttling.
- **Observed result/outcome**: Cloud without credits ran at 9,910.12µs vs 9,485.34µs with credits (+4.5% execution time increase), validating the performance degradation under credit depletion.

## [2026-09-15T22:15:00+07:00] - Part 3: Comparison Plot Generation
- **Topic**: Generate Matplotlib Comparison Plot for all 3 scenarios.
- **What was attempted**: Created and executed `plot_comparison.py` to read `result.txt`, `result1.txt`, and `result2.txt` from `result_credit/`, plotting elapsed time vs iterations (0 to 50,000) and exporting to `comparison_plot.png` at 300 DPI.
- **Hypothesis being tested**: The plotted curves will visually illustrate the execution slopes across all 3 scenarios (Cloud with Credits being the lowest/fastest curve, Cloud No Credits slightly higher, and Physical Machine highest/slowest).
- **Observed result/outcome**: `comparison_plot.png` was successfully generated with clear visualization matching lecture slide 89 specifications.
