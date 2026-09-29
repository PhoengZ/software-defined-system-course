# Activity Log

## [2026-09-29 13:52] Initialization & Analysis of Activity 7
- **Topic**: Activity 7 Storage System Performance Planning
- **Attempted**: 
  - Inspected `Activity7_2026-172259-17905645498670.pdf` and `Act_2_setup_guide-172259-17246496102189.pdf`.
  - Verified directory contents: found test files (2KiB, 256KiB, 1MiB, 128MiB).
  - Drafted comprehensive First Plan (Initialize Plan) detailing Manual vs Code steps, AWS credentials configuration (`C:\Users\USER\.aws\credentials`), local venv setup with `requirements.txt` (`boto3`), and benchmark code structure.
- **Hypothesis**: The activity requires testing storage throughput across EBS, Ephemeral NVMe, and S3 using EC2 `c6gd.medium` (ARM64) and Python (`test_fs.py`, `test_s3.py`). S3 credentials can be configured locally at `C:\Users\USER\.aws\credentials` for local testing/scripting, and least-privilege IAM policy is needed.
- **Observed Result**: User cannot yet access the Google Spreadsheet link. First Plan created; awaiting user confirmation and spreadsheet attachment before proceeding to Second Plan.

## [2026-09-29 13:58] Configured .gitignore to Ignore .txt Data Files
- **Topic**: Repository Hygiene & Preventing Commitment of Benchmark Data Files
- **Attempted**: Created `act7/.gitignore` to ignore `*.txt`, `*.dat`, `*.bin`, `.venv/`, credentials, and temporary benchmark outputs.
- **Hypothesis**: Adding `*.txt` to `act7/.gitignore` prevents large data files (`random_large...txt`, `1MiB...txt`, etc.) from being accidentally tracked or committed to Git.
- **Observed Result**: `git status` confirmed that all `.txt` data files are now ignored and only `.gitignore` is tracked as untracked file.

## [2026-09-29 14:02] Created FIRST_PLAN.md in Current Directory
- **Topic**: Activity 7 First Plan Document Creation
- **Attempted**: Created `FIRST_PLAN.md` directly in the project root directory detailing the Manual vs Code steps, AWS credential setup at `C:\Users\USER\.aws\credentials`, virtual environment creation, benchmark code specifications, and the spreadsheet verification gate.
- **Hypothesis**: Having `FIRST_PLAN.md` within the current directory allows the user to review the full initialize plan locally and establishes the formal gate for receiving the spreadsheet before Second Plan generation.
- **Observed Result**: `FIRST_PLAN.md` created successfully. Awaiting user review, plan confirmation, and spreadsheet attachment.

## [2026-09-29 14:14] Refactored FIRST_PLAN.md to Adopt Method 2 (IAM Role for EC2)
- **Topic**: Architecture Alignment with Assignment Requirements (IAM Role vs Local Credentials)
- **Attempted**: Updated `FIRST_PLAN.md` and `initial_implementation_plan.md` to establish Method 2 (IAM Role for EC2 Instance Profile with least-privilege S3 Policy) as the primary credential mechanism, directly fulfilling the lab requirement ("set up your credentials using roles") and Question 6.
- **Hypothesis**: Adopting IAM Role eliminates hardcoded/stored long-term credentials on EC2, utilizes IMDS for temporary security tokens, and adheres to AWS Best Practice.
- **Observed Result**: Plan successfully refactored and aligned with user instruction and assignment specification.

## [2026-09-29 14:42] Analysis of 2110415 Storage Benchmark Template.xlsx & Second Plan Architecture
- **Topic**: Spreadsheet Parameter Extraction, Metrics Formulation & Teardown Architecture
- **Attempted**: 
  - Extracted exact experiment matrix from `2110415 Storage Benchmark Template.xlsx`:
    - 2 KiB: EBS/Ephemeral (N = 32768, 65536, 131072, 262144, 393216); S3 (N = 512, 1024, 2048, 4096, 6144)
    - 256 KiB: EBS/Ephemeral/S3 (N = 512, 1024, 2048, 4096, 6144)
    - 1 MiB: EBS/Ephemeral/S3 (N = 128, 256, 512, 1024, 1536)
    - 128 MiB: EBS/Ephemeral/S3 (N = 1, 2, 4, 8, 12)
  - Formulated explicit mathematical derivations for all table columns: Total write time ($t_1 - t_0$), Write time per file ($\frac{\text{Total Time}}{N}$), and Bandwidth ($\frac{\text{Total Data}}{\text{Total Time}}$).
  - Designed resource lifecycle and safe teardown protocol (EC2 instance, EBS root volume, S3 objects/bucket, IAM role/policy, Security Groups, Key Pairs) guaranteeing $0 ongoing AWS expenditure after data capture.
- **Hypothesis**: Having the exact matrix from the spreadsheet enables precise automation scripting and accurate data export back to Excel. AWS resources can be safely and completely dismantled once spreadsheet cells are filled, leaving graph plotting and analysis to run offline.
- **Observed Result**: Spreadsheet parameters successfully mapped. Ready to present Implementation Plan and deliver Second Plan upon user verification.

## [2026-09-29 14:44] User Directive: Single-Run Policy to Minimize AWS Cost
- **Topic**: Benchmark Execution Strategy Adjustment
- **Attempted**: 
  - Adjusted benchmark plan to execute exactly 1 single trial per scenario ($N$ value) instead of running 3 trials with averaging.
  - Aligned rationale: Reduces total S3 API calls (PutObject requests cost $0.005 per 1,000 requests) and EC2 runtime, cutting AWS expenditure to the absolute minimum while strictly fulfilling all cells in `2110415 Storage Benchmark Template.xlsx`.
- **Hypothesis**: A single carefully executed run per configuration provides empirical data directly usable for `Total write time`, `Write time per file`, and `Bandwidth (MB/s)` without redundant cost.
- **Observed Result**: Constraint integrated into `SECOND_PLAN.md` and automation scripts.
