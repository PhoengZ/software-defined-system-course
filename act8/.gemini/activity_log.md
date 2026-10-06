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
## [2026-10-06 20:06:00 +07:00] - Implementation Plan Formulation for www.chula.ac.th Slide 4-5 Documentation

- **Topic:** Structuring the Markdown documentation and Mermaid architecture diagram for Slide 4-5 (www.chula.ac.th).
- **What was attempted:** Formulated a comprehensive implementation plan to generate `slide_4_5_www_chula.md` containing the Mermaid architecture diagram and in-depth technical descriptions for the 3 required slide points (Final Architecture Design, Pros & Cons, and Remaining Shortcomings vs On-Premise).
- **Hypothesis being tested:** Structuring the content with ready-to-copy bullet points and a clean Mermaid diagram will allow direct transfer into presentation slides while adhering strictly to course requirements and verification gates.
- **The observed result/outcome:** Implementation plan drafted covering all 4 architectural layers (Edge/CDN, Compute, Database, Storage) and 3 assignment questions. Presenting plan to user for verification gate.
## [2026-10-06 20:07:00 +07:00] - Created slide_4_5_www_chula.md Documentation

- **Topic:** Generation of Slide 4-5 documentation for www.chula.ac.th.
- **What was attempted:** Generated `slide_4_5_www_chula.md` containing the Mermaid architecture diagram, 4-layer breakdown, Multi-cloud rationale, comprehensive Pros/Cons evaluation, and specific remaining shortcomings compared to on-premise baseline.
- **Hypothesis being tested:** Providing a structured, copy-paste ready Markdown file with slide layout mapping will directly fulfill the assignment specifications for Slides 4 and 5.
- **The observed result/outcome:** Successfully created `slide_4_5_www_chula.md`. The documentation is ready for presentation slide authoring.
## [2026-10-06 20:20:00 +07:00] - Implementation Plan for Old vs New Architecture Mermaid Comparison

- **Topic:** Designing comparative Mermaid architecture diagrams (Old On-Premise vs New Multi-Cloud) in `slide_4_5_www_chula.md`.
- **What was attempted:** Formulated an implementation plan to enhance `slide_4_5_www_chula.md` by adding a dedicated On-Premise baseline Mermaid diagram alongside the Multi-Cloud diagram, with explicit layer-by-layer visual callouts highlighting bottlenecks (SPOF, bandwidth constraints, stateful coupling) versus cloud architectural benefits (edge caching, stateless auto-scaling, decoupled object storage).
- **Hypothesis being tested:** Visualizing both old and new architectures side-by-side will clearly demonstrate the structural contrast required for Slide 4-5.
- **The observed result/outcome:** Implementation plan created. Presenting to user for verification gate prior to updating `slide_4_5_www_chula.md`.
## [2026-10-06 20:21:00 +07:00] - Updated slide_4_5_www_chula.md with Old vs New Mermaid Diagrams

- **Topic:** Integration of dual architecture diagrams (Old On-Premise vs New Multi-Cloud) in `slide_4_5_www_chula.md`.
- **What was attempted:** Updated `slide_4_5_www_chula.md` to include:
  1. Mermaid diagram for Old On-Premise Monolithic architecture highlighting single points of failure, network bottlenecks, and coupled disk storage.
  2. Mermaid diagram for New Multi-Cloud architecture with Anycast DNS, Multi-CDN, stateless containers, decoupled object storage, and cross-cloud database DR replication.
  3. Layer-by-layer architectural transformation table.
  4. Updated Slide 4 layout guidance showing side-by-side Before/After presentation format.
- **Hypothesis being tested:** Visualizing both architectures side-by-side demonstrates clear contrast and allows seamless transfer into Slide 4 and Slide 5.
- **The observed result/outcome:** Successfully updated `slide_4_5_www_chula.md` with both Mermaid diagrams and comparative analysis.
## [2026-10-06 20:25:00 +07:00] - Implementation Plan for Compact Mermaid Architecture Diagrams

- **Topic:** Optimizing Mermaid diagram layout in `slide_4_5_www_chula.md` to be compact and screenshot-friendly within 1 page.
- **What was attempted:** Formulated an implementation plan to re-engineer both Old and New architecture diagrams by switching from sprawling vertical `flowchart TD` to horizontal `flowchart LR` / compact side-by-side layout, shortening node text, and providing a unified single-diagram comparison option that can be captured in a single 16:9 screenshot.
- **Hypothesis being tested:** A streamlined horizontal layout with concise labels and side-by-side comparison will drastically reduce diagram height and fit perfectly within a single slide or capture window.
- **The observed result/outcome:** Implementation plan drafted. Presenting to user for verification gate.
