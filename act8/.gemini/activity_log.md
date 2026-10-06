# Activity Log

## [2026-10-06 19:55:00 +07:00] - Review Activity 8 Assignment Requirements and System Architecture Analysis

- **Topic:** Activity 8: Multi-cloud and hybrid cloud architectures analysis for Reg Chula and www.chula.ac.th.
- **What was attempted:** Inspected the PDF assignment `Activity8-172259-17609631643493.pdf` to understand the presentation requirements, constraints, and hints for reverse engineering or analyzing current on-premise architectures.
- **Hypothesis being tested:** The assignment does not require black-box hacking or deep reverse engineering of production systems, but rather relies on course lecture hints (MyCourseVille playlist), system characteristics deduction (transactional vs content-driven), and standard software-defined / cloud architectural patterns.
- **The observed result/outcome:** The PDF specifically includes a hint pointing to the MyCourseVille playlist about Reg Chula. For www.chula.ac.th, architecture can be inferred from standard university web portal workloads. No intrusive reverse engineering is required; passive inspection and architectural deduction are sufficient.
## [2026-10-06 20:02:00 +07:00] - Reverse Engineering and Architectural Deduction for www.chula.ac.th

- **Topic:** Deduction of www.chula.ac.th on-premise baseline and final cloud architecture design.
- **What was attempted:** Ran DNS inspection and HTTP header probing on `www.chula.ac.th` to identify technology stack (revealed WordPress CMS with Imperva WAF/CDN frontend) and deduced the baseline on-premise architecture and appropriate final cloud architecture (Multi-Cloud / Hybrid Cloud).
- **Hypothesis being tested:** www.chula.ac.th can be mapped to a standard Read-heavy Content-driven Web Portal architecture without requiring access to internal source code or internal server configs.
- **The observed result/outcome:** HTTP response confirmed `wp-json` (WordPress CMS) and Imperva CDN. The on-premise baseline is an on-premise LAMP/LEMP stack in Chula's data center. The optimal final architecture is Multi-Cloud (stateless containerized WordPress + Multi-CDN + S3/GCS Object Storage + Managed Relational DB), which is straightforward compared to Reg Chula's transactional ACID requirements.
