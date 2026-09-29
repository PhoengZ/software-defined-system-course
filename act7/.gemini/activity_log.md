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
