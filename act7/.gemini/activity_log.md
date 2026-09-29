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

## [2026-09-29 14:55] Analysis of Required Metrics for Answering Activity 7 Questions
- **Topic**: Data Scope Validation (Spreadsheet Metrics vs System Metrics / CPU Usage)
- **Attempted**: Analyzed `Activity7_2026-172259-17905645498670.pdf` questions 1-7 against system monitoring requirements.
- **Hypothesis**: The benchmark is entirely I/O bound. Only spreadsheet metrics (`Total write time`, `Write time per file`, `Bandwidth`, file sizes, and iterations $N$) plus IAM policy JSON and architectural theory are required to answer all 7 questions. CPU usage is irrelevant and not required. EC2 CloudWatch EBS monitoring is mentioned only as optional additional insight.
- **Observed Result**: Clarified metric scope to user: CPU usage is not needed; empirical spreadsheet data is fully sufficient.

## [2026-09-29 14:58] Architecture Breakdown of Python Scripts & Instance Deployment Strategies
- **Topic**: Script Roles and File Transfer Methodology
- **Attempted**: 
  - Defined explicit roles for `test_fs.py`, `test_s3.py`, `benchmark_runner.py`, and `sync_to_excel.py`.
  - Analyzed file deployment options: Compared manual copy-pasting via `vim` against secure copy (`scp`) and VS Code Remote SSH.
- **Hypothesis**: While code could technically be pasted into `vim`, `scp` is vastly superior and required anyway because the 4 test data files (especially 128 MiB binary file) cannot be copy-pasted via terminal clipboard without truncation or corruption.
- **Observed Result**: Documented clear workflow recommending `scp` single-command transfer alongside vim instructions if preferred.

## [2026-09-29 15:07] Root Cause Analysis: AWS SCP Explicit Deny on access-analyzer:ValidatePolicy
- **Topic**: IAM Console Policy Creation Error Investigation
- **Attempted**: Analyzed error `access-analyzer:ValidatePolicy with an explicit deny in a service control policy (SCP)`.
- **Hypothesis**: The user's account belongs to an AWS Organization (likely AWS Academy or university lab sandbox). In the AWS Console JSON editor, IAM Access Analyzer is automatically called in real time to validate policy syntax. The Organization's SCP explicitly denies `access-analyzer:*`. Furthermore, student lab environments often restrict custom IAM role/policy creation and provide a pre-existing role (`LabRole`).
- **Observed Result**: Formulated 2-tier resolution: (1) Test if pressing "Next" or using CLI bypasses the real-time validator, and (2) If SCP blocks IAM creation entirely, check for the standard pre-configured `LabRole` in the account.

## [2026-09-29 15:09] Confirmation of Policy Creation Workflow
- **Topic**: IAM Policy Validation Bypass Confirmation
- **Attempted**: Advised user that if the policy can be saved and created successfully by pressing "Next", the Access Analyzer error was purely a real-time UI notification that does not impede policy creation or subsequent role attachment.
- **Hypothesis**: The IAM Policy will function normally when attached to an IAM Role and EC2 instance profile once created.
- **Observed Result**: User proceeding to create Role and launch EC2 instance.

## [2026-09-29 15:16] Regional Alignment: Enforcing ap-southeast-2 (Sydney)
- **Topic**: AWS Academy Regional Locking & Performance Isolation
- **Attempted**: Addressed user finding that S3 Bucket region is defaulted/locked to `Asia Pacific (Sydney) ap-southeast-2`.
- **Hypothesis**: AWS Academy / Lab accounts restrict resource provisioning to designated regions (Sydney in this course). To prevent cross-region network latency (which would unfairly throttle S3 benchmark times), the EC2 `c6gd.medium` instance must be provisioned in the exact same region (`ap-southeast-2`).
- **Observed Result**: Advised user to accept `ap-southeast-2` and verify that the EC2 Console region selector is also set to Sydney before launching.

## [2026-09-29 15:27] Analysis of EC2 Free Tier Warning for c6gd.medium
- **Topic**: EC2 Instance Selection & Billing Clarification
- **Attempted**: Investigated user report stating that `c6gd.medium` is not covered by the free tier/plan.
- **Hypothesis**: The AWS Console displays an informational badge indicating non-eligibility for the AWS 12-month Free Tier (which only covers `t2.micro`/`t3.micro`). In course/lab accounts, `c6gd.medium` is specifically mandated by the professor for Ephemeral NVMe access and is paid via course lab credits (~$0.0384/hr). If it is purely a UI warning, user can proceed to launch; if it is a hard quota error upon clicking Launch, subnet/AZ adjustment or quota check is needed.
- **Observed Result**: Clarified the distinction between the Free Tier warning and a launch-blocking error.

## [2026-09-29 15:29] Troubleshooting Grayed-out c6gd.medium (Architecture & Filter Check)
- **Topic**: EC2 Instance Selector Incompatibility Diagnosis
- **Attempted**: Investigated why `c6gd.medium` is grayed out in the selection dropdown.
- **Hypothesis**:
  1. Primary cause: AMI Architecture is set to default `64-bit (x86)` instead of `64-bit (Arm)`. Since `c6gd` runs on ARM Graviton2, AWS Console grays out all Arm instances when x86 is selected (as warned in `Act_2_setup_guide` page 2).
  2. Secondary cause: A filter such as "Free tier eligible" is enabled in the instance type dropdown, or the user's account has a strict course plan restriction.
- **Observed Result**: Provided clear visual steps for changing AMI architecture to 64-bit (Arm) and clearing instance type filters.

## [2026-09-29 15:33] Instance Unlocked & Billing Credit Priority Confirmation
- **Topic**: AWS Promotional/Lab Credit Deduction Mechanism
- **Attempted**: Confirmed to user that `c6gd.medium` is unlocked and clarified AWS credit consumption order.
- **Hypothesis**: AWS billing systems strictly deduct from promotional/lab credits first before billing any credit card or external payment method. Running `c6gd.medium` (~$0.0384/hr) for the duration of this single-trial benchmark will consume only a negligible amount of credits.
- **Observed Result**: Reassured user and prepared to guide through SSH, NVMe mounting, and benchmark execution.

## [2026-09-29 15:36] Storage Architecture Clarification: EBS vs Ephemeral vs S3 Attachment
- **Topic**: Storage Attachment Mechanism
- **Attempted**: Clarified user inquiry regarding why they don't explicitly attach bucket, EBS, or ephemeral storage during EC2 launch.
- **Hypothesis**:
  1. EBS: The 60 GB Volume 1 specified during launch IS the EBS Root Volume (gp3).
  2. Ephemeral Storage: Physically direct-attached NVMe SSD (~59 GB) included automatically with `c6gd.medium` hardware; requires POSIX formatting (`mkfs.ext4`) and mounting (`mount`) inside Linux OS.
  3. Amazon S3: Object storage accessed over HTTPS REST API via IAM Role/Profile permissions, never mounted as a block device.
- **Observed Result**: Clearly articulated the 3 distinct storage access models.
