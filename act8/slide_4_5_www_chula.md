# สถาปัตยกรรมสำหรับ Slide 4-5: www.chula.ac.th (Activity 8)
**วิชา:** 2110415 Software-Defined Systems  
**หัวข้อ:** Comparison of Old (On-Premise) vs New (Multi-Cloud) Architecture for `www.chula.ac.th`

---

## 1. เปรียบเทียบแผนภาพสถาปัตยกรรม (Compact Architecture Diagrams)

> [!TIP]
> **สำหรับแคปเจอร์ภาพลงสไลด์:** แผนภาพด้านล่างถูกออกแบบให้มีขนาดกะทัดรัด (Compact Layout) จัดเรียงแนวนอน เพื่อให้สามารถแคปหน้าจอลงสไลด์อัตราส่วน 16:9 ได้ครบถ้วนภายใน 1 หน้าจอโดยไม่ต้อง Scroll

### 1.1 แบบรวมภาพเดียว (Unified Single Diagram: แนะนำสำหรับใส่ใน Slide 4)
*แคปภาพบล็อกนี้เพียงรูปเดียว จะเห็นวิวัฒนาการเปรียบเทียบ "เก่า vs ใหม่" ได้ทันที:*

```mermaid
flowchart TB
    subgraph OLD ["🔴 สถาปัตยกรรมเดิม: On-Premise Monolithic (SPOF & Bottlenecks)"]
        direction LR
        U1["ผู้ใช้งานทั่วไป\n(Global & Local)"] -->|"Direct HTTP"| GW["Campus Gateway & Firewall\n(🔴 คอขวด Bandwidth ขาเข้า)"]
        GW --> SVR["Monolithic Web/App Server\n+ Local Disk /uploads/\n(🔴 ขยายเครื่องไม่ได้ / SPOF)"]
        SVR --> DB1[("On-Premise MySQL\n(🔴 Single Database / SPOF)")]
    end

    subgraph NEW ["🟢 สถาปัตยกรรมใหม่: Modern Multi-Cloud (High Availability & Elastic)"]
        direction LR
        U2["ผู้ใช้งานทั่วไป\n(Global Access)"] --> DNS["Anycast DNS / GSLB\n(Route 53 / Cloudflare)"]
        DNS --> CDN["Multi-CDN & WAF\n(CloudFront + Cloud CDN)\n(🟢 แคชที่ Edge >90%)"]
        
        subgraph CLOUD_RUN ["Multi-Cloud Auto-scaling (AWS + GCP)"]
            direction TB
            AWS["AWS Thailand:\nECS Fargate + S3 Media + Aurora MySQL (Primary)"]
            GCP["GCP Thailand:\nCloud Run + GCS Media + Cloud SQL (Standby DR)"]
            AWS <-.->|"Cross-Cloud Sync & DB Replication"| GCP
        end
        
        CDN -->|"Cache Miss Only"| CLOUD_RUN
    end

    classDef redBox fill:#ffebee,stroke:#c62828,stroke-width:1.5px;
    classDef greenBox fill:#e8f5e9,stroke:#2e7d32,stroke-width:1.5px;
    class GW,SVR,DB1 redBox;
    class CDN,CLOUD_RUN,AWS,GCP greenBox;
```

---

### 1.2 แบบแยกภาพเดี่ยวแนวนอน (Separate Horizontal Diagrams: สำหรับแคปแยกภาพ)

#### (ก) สถาปัตยกรรมเดิม (Old Architecture - On-Premise)
```mermaid
flowchart LR
    User["ผู้ใช้งาน\n(Global Public)"] -->|"Direct Traffic"| GW["Campus Gateway & Firewall\n(🔴 Bandwidth Bottleneck)"]
    GW --> Web["On-Premise VM Server\n(Monolithic WordPress + Local Disk)\n(🔴 SPOF / Fixed Capacity)"]
    Web --> DB[("MySQL Database Server\n(🔴 Single Instance / No Failover)")]

    classDef red fill:#ffebee,stroke:#c62828,stroke-width:1.5px;
    class GW,Web,DB red;
```

#### (ข) สถาปัตยกรรมใหม่ (New Architecture - Multi-Cloud)
```mermaid
flowchart LR
    User["ผู้ใช้งาน\n(Global Access)"] --> DNS["Global Anycast DNS / GSLB\n(Route 53 / Cloudflare)"]
    DNS --> CDN["Multi-CDN & WAF Layer\n(🟢 Edge Caching >90-95%)"]
    
    CDN -->|"Primary (Active)"| AWS["AWS Thailand:\nStateless Containers + S3 + Aurora DB"]
    CDN -.->|"Failover (DR)"| GCP["GCP Thailand:\nStateless Containers + GCS + Cloud SQL"]
    
    AWS <-.->|"Async DB Replication & Storage Sync"| GCP

    classDef green fill:#e8f5e9,stroke:#2e7d32,stroke-width:1.5px;
    class CDN,AWS,GCP green;
```

---

### 1.3 ตารางเปรียบเทียบสถาปัตยกรรมระดับ Layer (Architectural Transformation)

| Architectural Layer | สถาปัตยกรรมเดิม (On-Premise) | สถาปัตยกรรมใหม่ (Multi-Cloud) | ผลลัพธ์เชิงสถาปัตยกรรม |
| :--- | :--- | :--- | :--- |
| **Ingress & Caching** | วิ่งตรงผ่าน Campus Gateway ของจุฬาฯ ไม่มี CDN สากล | **Anycast DNS + Multi-CDN (CloudFront + Cloud CDN)** | ตัดภาระโหลดของ Origin Server ได้กว่า 90-95% โหลดเร็วทั่วโลก |
| **Compute & Scaling** | Monolithic VM เครื่องเดียว ขยายเครื่องไม่ได้ทันที | **Stateless Containers (ECS / Cloud Run)** Auto-scaling | ยืดหดเครื่องอัตโนมัติตามปริมาณข่าวด่วน (Elastic) ในระดับนาที |
| **Storage & Assets** | Local Server Disk / NAS (`wp-content/uploads`) | **Decoupled Object Storage (AWS S3 + GCP GCS Sync)** | แยกไฟล์มีเดียออกจากเซิร์ฟเวอร์ ทนทานระดับ 99.999999999% |
| **Database & State** | Single MySQL Instance ในศูนย์คอมฯ จุฬาฯ | **Managed Aurora MySQL + Standby Cloud SQL** | ทำ Disaster Recovery ข้ามคลาวด์ ป้องกันฐานข้อมูลล่ม 100% |
| **High Availability** | ขึ้นอยู่กับ Data Center จุฬาฯ (SPOF สูง) | **Multi-Provider Resiliency (AWS + GCP)** | คลาวด์ค่ายใดค่ายหนึ่งล่ม อีกเจ้าทำงานต่อได้ทันที (Uptime 99.99%+) |

---

## 2. ข้อ 1: การออกแบบ Final Architecture (Multi-Cloud Pattern)

### ทำไมถึงเลือก "Multi-Cloud" แทน "Hybrid Cloud"?
1. **ธรรมชาติของระบบ (Public Read-Heavy Portal):**  
   `www.chula.ac.th` เป็นเว็บประชาสัมพันธ์และหน้าตาของมหาวิทยาลัย ข้อมูลทั้งหมดเป็นสาธารณะ (Public Data) ไม่มีความลับของข้อมูลนิสิตหรือข้อจำกัดด้าน PDPA ที่จำเป็นต้องเก็บกักไว้ใน Local On-Premise เหมือนระบบทะเบียน (`Reg Chula`)
2. **ความต้องการด้าน Uptime และ Disaster Recovery ระดับสูงสุด:**  
   หากเกิดภัยพิบัติหรือ Cloud เจ้าใดเจ้าหนึ่งล่มทั้ง Region ระบบจะสามารถ Failover ไปยัง Cloud อีกเจ้าได้ทันที ทำให้เว็บมหาวิทยาลัยมี Uptime 99.99%+ ตลอดเวลา
3. **กำจัดคอขวดของ On-premise อย่างสิ้นเชิง:**  
   ไม่ต้องพึ่งพาระบบเครือข่ายหรือห้องเซิร์ฟเวอร์ภายในมหาวิทยาลัย

### รายละเอียดการทำงานของแต่ละ Layer:
* **Layer 1: Global Routing & Multi-CDN Layer:**
  * ใช้ **Global Server Load Balancing (GSLB)** ตรวจเช็ค Health check ตลอดเวลา หากเกิดเหตุขัดข้องจะสลับ DNS ไปยังคลาวด์สำรองโดยอัตโนมัติ
  * แคชเนื้อหาข่าว สารสนเทศ รูปภาพ และไฟล์สถิติไว้ที่ Edge Servers ทั่วโลก ทราฟฟิกกว่า **90-95% จะถูกส่งจาก Edge ทันที** โดยไม่ต้องวิ่งเข้าเครื่องเซิร์ฟเวอร์
* **Layer 2: Compute Layer (Stateless Web Containers):**
  * สถาปัตยกรรม WordPress ถูกแยกให้เป็น **Stateless (ไร้สถานะ)** ทั้งหมด
  * รันบน Container (AWS Fargate และ GCP Cloud Run/GKE) พร้อมระบบ **Horizontal Pod Autoscaling (HPA)** ที่ยืดหดจำนวนเซิร์ฟเวอร์ได้อัตโนมัติตามโหลดผู้ใช้งาน
* **Layer 3: Storage Layer (Decoupled Assets):**
  * ไฟล์รูปภาพ ข่าวสาร และเอกสาร PDF (`wp-content/uploads`) ถูกแยกออกจากเซิร์ฟเวอร์ไปเก็บใน Object Storage (AWS S3) และซิงก์แบบสองทางไปยัง Google Cloud Storage (GCS)
* **Layer 4: Database Layer (Cross-Cloud DR):**
  * ใช้ Managed Relational Database (Amazon Aurora MySQL) เป็นโหนดหลัก (Active Read/Write) สำหรับแอดมินโพสต์ข่าว และทำ Async Replication ข้ามไปยัง Google Cloud SQL เป็นตัวสำรอง (Standby/DR)

---

## 3. ข้อ 2: การวิเคราะห์ข้อดีและข้อเสีย (Pros & Cons)

### ข้อดี (Pros):
1. **High Availability & Fault Tolerance สูงสุด (Zero Single Point of Failure):**  
   ไม่มีจุดล่มจุดเดียว หากระบบของ AWS ขัดข้อง ระบบจะสลับไปยัง GCP อัตโนมัติ เว็บมหาวิทยาลัยไม่มีวันดับ
2. **Near-Infinite Scalability (รองรับ Spike สบาย):**  
   เมื่อเกิดเหตุการณ์สำคัญระดับประเทศ (เช่น วันประกาศ TCAS, ข่าวด่วนมหาวิทยาลัย, งานพระราชทานปริญญาบัตร) Auto-scaling จะเพิ่มเครื่องรองรับผู้ใช้งานหลักแสนได้ภายในเวลาไม่กี่นาที
3. **Global Performance & Low Latency:**  
   ชาวต่างชาติ สถาบันจัดอันดับมหาวิทยาลัยโลก (QS / THE World University Rankings) หรือนิสิตต่างชาติเปิดดูเว็บได้เร็วเท่ากับคนในประเทศไทย เพราะข้อมูลถูกส่งจาก Edge CDN ที่อยู่ใกล้ที่สุด
4. **ป้องกันการโจมตีระดับ Terabits (DDoS Protection):**  
   Cloud WAF และ CDN ช่วยกรองบอทและการยิง DDoS ให้จบตั้งแต่ระดับ Edge โดยไม่กระทบเซิร์ฟเวอร์จริง
5. **No On-premise Hardware Maintenance:**  
   บุคลากรไอทีมหาวิทยาลัยไม่ต้องเสียเวลากับการเปลี่ยนอะไหล่ฮาร์ดดิสก์ แอร์ห้องเซิร์ฟเวอร์ดับ หรือระบบสำรองไฟสำรอง

### ข้อเสีย (Cons):
1. **Operational & Architectural Complexity:**  
   การดูแลระบบข้าม 2 Cloud ผู้ดูแลระบบต้องมีทักษะระดับสูง เช่น การเขียน Infrastructure as Code (Terraform), การจัดการ CI/CD และความเข้าใจคอนฟิกทั้ง AWS และ Google Cloud
2. **Cross-Cloud Data Transfer Cost (Egress Fee):**  
   มีค่าใช้จ่ายในการถ่ายโอนข้อมูลข้ามคลาวด์ โดยเฉพาะการ Replicate ข้อมูล Database และการ Sync สตอเรจมีเดียข้ามค่าย
3. **Data Consistency Latency:**  
   การจำลองฐานข้อมูลข้ามคลาวด์เป็นแบบ Asynchronous อาจมีความล่าช้าในการ Sync เล็กน้อย (เสี้ยววินาที) หากเกิด Failover กะทันหัน

---

## 4. ข้อ 3: Shortcomings ที่ยังคงเหลืออยู่เมื่อเทียบกับ On-Premise

สิ่งที่อาจารย์เน้นถามในโจทย์คือ **"แม้จะย้ายขึ้น Cloud สถาปัตยกรรมใหม่นี้ยังมีจุดด้อยอะไรเมื่อเทียบกับ On-premise ดั้งเดิม?"**:

1. **การเปลี่ยนรูปแบบต้นทุนจากคงที่เป็นแบบผันแปร (Opex vs Capex) & เสี่ยง Bill Shock:**  
   * *On-premise:* เป็นต้นทุนคงที่ (Capex) จ่ายค่าเซิร์ฟเวอร์ครั้งเดียว คำนวณงบประมาณรายปีของมหาวิทยาลัยได้แน่นอน  
   * *Multi-Cloud:* เป็นต้นทุนแปรผันตามการใช้งานจริง (Opex) หากเว็บถูกบอทสแครป หรือทีมงานคอนฟิก CDN Cache Policy ผิดพลาดจนรีเควสต์หลุดมาที่ Origin อาจทำให้งบประมาณคลาวด์พุ่งสูงเกินควบคุม
2. **การสูญเสียการควบคุมระดับกายภาพ (Loss of Low-Level Infrastructure Control):**  
   * มหาวิทยาลัยไม่สามารถเข้าถึงหรือควบคุม Hardware/Hypervisor ได้โดยตรง ต้องพึ่งพาข้อตกลงระดับบริการ (SLA) ของผู้ให้บริการคลาวด์ หากเกิดปัญหาเชิงลึกระดับคลาวด์ทำได้เพียงรอทาง Provider แก้ไข
3. **ต้องปรับทักษะของบุคลากรภายใน (Staff Reskilling):**  
   * บุคลากรฝ่ายไอทีของมหาวิทยาลัยที่คุ้นเคยกับการดูแล System Admin แบบ On-premise ดั้งเดิม ต้องปรับตัวและผ่านการเทรนทักษะด้าน Cloud Architecture และ Cloud Security อย่างหนัก

---

## 5. สรุปเนื้อหาสำหรับจัดใส่ Slide 4 และ Slide 5 (Presentation Ready)

### 📌 Slide 4: Architecture Evolution (Old vs New Architecture)
* **หัวข้อสไลด์:** Evolution of Architecture for `www.chula.ac.th` (On-Premise vs Multi-Cloud)
* **การวางภาพประกอบ:** นำภาพจากข้อ **1.1 (Unified Single Diagram)** หรือนำภาพจากข้อ **1.2 (วางซ้าย-ขวา)** มาแปะลงสไลด์
* **Bullet Points อธิบายสไลด์:**
  * ปรับเปลี่ยนจาก Monolithic On-Premise สู่ **Multi-Cloud (AWS + GCP)** เพื่อกำจัด Single Point of Failure
  * ข้อมูลข่าวสารเป็น Public Content จึงแคชไว้ที่ Multi-CDN Edge ได้มากกว่า 90-95%
  * ใช้ Stateless Containers ร่วมกับ Auto-scaling เพื่อรองรับทราฟฟิกข่าวด่วนได้ทันที

---

### 📌 Slide 5: Evaluation (Pros, Cons & Remaining Shortcomings)
* **หัวข้อสไลด์:** Architectural Evaluation & Trade-offs
* **ตารางสรุปเปรียบเทียบ:**

| มิติการประเมิน | On-Premise ดั้งเดิม | Multi-Cloud ใหม่ |
| :--- | :--- | :--- |
| **High Availability** | ⚠️ ต่ำ (เสี่ยงดับทั้งเว็บจากระบบไฟ/เน็ตเวิร์กจุฬาฯ) | ✅ **สูงมาก 99.99%+** (ทนทานต่อ Cloud ค่ายใดค่ายหนึ่งล่ม) |
| **Scalability** | ⚠️ ตายตัวตามฮาร์ดแวร์ ขยายเครื่องไม่ทันทราฟฟิก | ✅ **Auto-scale ยืดหดได้ในระดับนาที** |
| **Global Access** | ⚠️ ช้าเมื่อเปิดจากต่างประเทศ | ✅ **เร็วทั่วโลกด้วย Multi-CDN Edge** |

* **Remaining Shortcomings (ข้อจำกัดที่ยังเหลืออยู่เมื่อเทียบกับ On-Premise):**
  1. **Cost Model Transition:** เปลี่ยนเป็น Opex จ่ายตามจริง เสี่ยงงบประมาณบานปลาย (Bill Shock) หากคอนฟิก CDN หลุด ต่างจาก On-premise ที่งบประมาณ Capex คงที่
  2. **Operational Overhead:** ซับซ้อนกว่า ต้องใช้ทีมงานที่เชี่ยวชาญ Multi-Cloud DevOps (Terraform / CI/CD)
  3. **Loss of Infrastructure Control:** มหาวิทยาลัยไม่ได้เป็นเจ้าของฮาร์ดแวร์ ต้องพึ่งพา SLA ของ Cloud Provider ภายนอก
